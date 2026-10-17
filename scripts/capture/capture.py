"""Capture screenshots and short clips of the Fufa app for the docs.

Runs against a local app (web on :3000, api on :3005) signed in as the
project's test user. Every image is reproducible: when the UI changes,
run this again and commit the new files.

    python scripts/capture/capture.py                 # every page
    python scripts/capture/capture.py create-an-agent # one page
    python scripts/capture/capture.py --no-clips      # screenshots only, reuse the last agent

Recording a clip creates real records in the local workspace (a new agent for
create-an-agent), so use --no-clips while you iterate on screenshots.

Needs Python Playwright with Chromium (the monorepo's apps/kb-worker venv has
it). Clips are encoded with the ffmpeg build that ships with Playwright.
"""

from __future__ import annotations

import base64
import glob
import os
import subprocess
import sys
import time
from pathlib import Path

from playwright.sync_api import Locator, Page, sync_playwright

APP = os.environ.get("FUFA_APP_URL", "http://localhost:3000")
EMAIL = "test@example.com"  # project test user, see apps/api/src/auth/index.ts
OTP = "000000"

DOCS = Path(__file__).resolve().parents[2]
SHOTS = DOCS / "src" / "assets" / "screens"
CLIPS = DOCS / "public" / "clips"
STATE = Path(__file__).with_name(".auth.json")

VIEWPORT = {"width": 1180, "height": 760}
SCALE = 2
FPS = 30

# Injected into every page: hide dev-only overlays, draw a cursor and a
# highlight ring that the scripts below move around.
STAGE_CSS = """
.tsqd-parent-container, [class*="TanStackRouterDevtools"], .tsr-devtools,
button[aria-label*="Tanstack" i], button[aria-label*="devtools" i] { display: none !important; }
#fd-cursor { position: fixed; z-index: 2147483647; left: 0; top: 0; width: 22px; height: 22px;
  pointer-events: none; transition: transform .55s cubic-bezier(.3,.7,.2,1); transform: translate(-40px,-40px); }
#fd-cursor svg { filter: drop-shadow(0 2px 3px rgba(0,0,0,.25)); }
#fd-ripple { position: fixed; z-index: 2147483646; width: 34px; height: 34px; margin: -17px 0 0 -17px;
  border-radius: 50%; background: rgba(155, 195, 60, .45); pointer-events: none; opacity: 0; }
#fd-ripple.on { animation: fd-rip .45s ease-out; }
@keyframes fd-rip { from { opacity: 1; transform: scale(.3); } to { opacity: 0; transform: scale(1.4); } }
#fd-ring { position: fixed; z-index: 2147483645; pointer-events: none; border-radius: 12px;
  box-shadow: 0 0 0 2.5px #9BC33C, 0 0 0 7px rgba(155,195,60,.28); display: none; }
"""

STAGE_JS = """
() => {
  if (document.getElementById('fd-cursor')) return;
  const s = document.createElement('style'); s.textContent = %s; document.head.appendChild(s);
  const c = document.createElement('div'); c.id = 'fd-cursor';
  c.innerHTML = '<svg width="22" height="22" viewBox="0 0 22 22"><path d="M3 2l15 8.2-6.6 1.6L8.6 19z" fill="#111" stroke="#fff" stroke-width="1.6" stroke-linejoin="round"/></svg>';
  const r = document.createElement('div'); r.id = 'fd-ripple';
  const g = document.createElement('div'); g.id = 'fd-ring';
  document.body.append(c, r, g);
}
""" % repr(STAGE_CSS)


IDS = Path(__file__).with_name(".ids.json")


def remember(key: str, value: str | None = None):
    """Keep ids made by a clip run, so --no-clips can shoot the same records."""
    import json
    data = json.loads(IDS.read_text()) if IDS.exists() else {}
    if value is not None:
        data[key] = value
        IDS.write_text(json.dumps(data, indent=2))
    return data.get(key)


def agent_id(url: str) -> str | None:
    return url.split("/agents/")[1].split("/")[0] if "/agents/agt_" in url else None


class Stage:
    """A signed-in page plus helpers for shots and clips."""

    def __init__(self, page: Page, name: str):
        self.page = page
        self.name = name
        self.shot_dir = SHOTS / name
        self.shot_dir.mkdir(parents=True, exist_ok=True)
        self.frames: list[tuple[float, bytes]] | None = None
        self.speed = 1.0
        self._clock = 0.0
        self._last = 0.0
        self.cursor = (VIEWPORT["width"] * 0.6, VIEWPORT["height"] * 0.7)

    # ---- navigation -------------------------------------------------
    def go(self, path: str, settle: int = 1800):
        self.page.goto(APP + path)
        self.page.wait_for_load_state("networkidle")
        self.page.wait_for_timeout(settle)
        self.stage()

    def stage(self):
        self.page.evaluate(STAGE_JS)
        x, y = self.cursor
        self.page.evaluate(f"document.getElementById('fd-cursor').style.transform='translate({x}px,{y}px)'")

    # ---- pointer ----------------------------------------------------
    def point(self, target: Locator, dx: float = 0.5, dy: float = 0.5):
        target.scroll_into_view_if_needed()
        b = target.bounding_box()
        x, y = b["x"] + b["width"] * dx, b["y"] + b["height"] * dy
        self.page.evaluate(f"document.getElementById('fd-cursor').style.transform='translate({x - 3}px,{y - 2}px)'")
        self.cursor = (x - 3, y - 2)
        self.wait(650)
        return x, y

    def click(self, target: Locator, pause: int = 450):
        x, y = self.point(target)
        self.page.evaluate(
            f"(() => {{ const r = document.getElementById('fd-ripple'); r.style.left='{x}px'; r.style.top='{y}px';"
            " r.classList.remove('on'); void r.offsetWidth; r.classList.add('on'); })()"
        )
        target.click()
        self.wait(pause)
        self.stage()

    def type(self, target: Locator, text: str, delay: int = 32):
        self.click(target, pause=200)
        target.press_sequentially(text, delay=delay)
        self.wait(500)

    def wait(self, ms: int):
        self.page.wait_for_timeout(ms)

    # ---- screenshots ------------------------------------------------
    def ring(self, target: Locator | None, pad: int = 4):
        if target is None:
            self.page.evaluate("document.getElementById('fd-ring').style.display='none'")
            return
        b = target.bounding_box()
        self.page.evaluate(
            "([x,y,w,h]) => Object.assign(document.getElementById('fd-ring').style,"
            " {display:'block', left:x+'px', top:y+'px', width:w+'px', height:h+'px'})",
            [b["x"] - pad, b["y"] - pad, b["width"] + pad * 2, b["height"] + pad * 2],
        )

    def shot(self, file: str, area: Locator | list | dict | None = None, highlight: Locator | None = None, pad: int = 16):
        """Save a crop of the screen. `area` is a locator, several locators (their union) or a clip dict."""
        self.page.evaluate("document.getElementById('fd-cursor').style.display='none'")
        self.ring(highlight)
        clip = None
        if isinstance(area, dict):
            clip = area
        elif area is not None:
            boxes = [a.bounding_box() for a in (area if isinstance(area, list) else [area])]
            x0, y0 = min(b["x"] for b in boxes), min(b["y"] for b in boxes)
            x1 = max(b["x"] + b["width"] for b in boxes)
            y1 = max(b["y"] + b["height"] for b in boxes)
            b = {"x": x0, "y": y0, "width": x1 - x0, "height": y1 - y0}
            x, y = max(b["x"] - pad, 0), max(b["y"] - pad, 0)
            clip = {"x": x, "y": y,
                    "width": min(b["width"] + pad * 2, VIEWPORT["width"] - x),
                    "height": min(b["height"] + pad * 2, VIEWPORT["height"] - y)}
        self.page.screenshot(path=str(self.shot_dir / file), clip=clip)
        self.ring(None)
        self.page.evaluate("document.getElementById('fd-cursor').style.display=''")
        print("  shot", self.shot_dir.relative_to(DOCS) / file)

    # ---- clips ------------------------------------------------------
    def record(self):
        """Start collecting screencast frames (compositor frames, not a video file)."""
        self.cdp = self.page.context.new_cdp_session(self.page)
        self.frames = []
        self._clock, self._last = 0.0, time.monotonic()

        def on_frame(ev):
            now = time.monotonic()
            self._clock += (now - self._last) / self.speed
            self._last = now
            self.frames.append((self._clock, base64.b64decode(ev["data"])))
            self.cdp.send("Page.screencastFrameAck", {"sessionId": ev["sessionId"]})

        self.cdp.on("Page.screencastFrame", on_frame)
        self.cdp.send("Page.startScreencast", {"format": "jpeg", "quality": 92,
                                               "maxWidth": VIEWPORT["width"] * SCALE,
                                               "maxHeight": VIEWPORT["height"] * SCALE})

    def fast(self, factor: float):
        """Play what happens next `factor` times faster in the clip (e.g. waiting on AI)."""
        now = time.monotonic()
        self._clock += (now - self._last) / self.speed
        self._last = now
        self.speed = factor

    def save_clip(self, tail_ms: int = 1200, width: int = 1440):
        self.fast(1)
        self.wait(tail_ms)
        self.cdp.send("Page.stopScreencast")
        frames, self.frames = self.frames or [], None
        if not frames:
            raise RuntimeError("no frames recorded")
        end = self._clock + (time.monotonic() - self._last)
        out = CLIPS / f"{self.name}.webm"
        out.parent.mkdir(parents=True, exist_ok=True)
        ffmpeg = sorted(glob.glob(os.path.expanduser("~/Library/Caches/ms-playwright/ffmpeg-*/ffmpeg-mac"))
                        + glob.glob(os.path.expanduser("~/.cache/ms-playwright/ffmpeg-*/ffmpeg-linux")))[-1]
        height = round(width * VIEWPORT["height"] / VIEWPORT["width"] / 2) * 2
        # Resample the variable-rate screencast to a constant frame rate, as one
        # MJPEG stream (this ffmpeg build has no pipe input).
        stream = out.with_suffix(".mjpeg")
        with open(stream, "wb") as f:
            i = 0
            for k in range(int(end * FPS)):
                while i + 1 < len(frames) and frames[i + 1][0] <= k / FPS:
                    i += 1
                f.write(frames[i][1])
        subprocess.run(
            [ffmpeg, "-y", "-loglevel", "error", "-f", "image2pipe", "-c:v", "mjpeg", "-framerate", str(FPS),
             "-i", str(stream), "-vf", f"scale={width}:{height}", "-c:v", "libvpx", "-b:v", "3M", "-crf", "8",
             "-qmin", "0", "-qmax", "30", "-deadline", "good", "-cpu-used", "1", "-an", str(out)],
            check=True,
        )
        stream.unlink()
        (CLIPS / f"{self.name}.jpg").write_bytes(frames[-1][1])
        print(f"  clip {out.relative_to(DOCS)} ({end:.1f}s, {out.stat().st_size // 1024} KB)")


def sign_in(browser):
    ctx = browser.new_context(viewport=VIEWPORT, device_scale_factor=SCALE,
                              storage_state=str(STATE) if STATE.exists() else None)
    page = ctx.new_page()
    page.goto(APP + "/inbox")
    page.wait_for_timeout(2000)
    if "/login" in page.url:
        page.fill("input[type=email]", EMAIL)
        page.get_by_role("button", name="Send verification code").click()
        page.wait_for_timeout(1500)
        page.locator("input").first.click()
        page.keyboard.type(OTP)
        page.get_by_role("button", name="Verify Code").click()
        page.wait_for_url(lambda u: "/login" not in u and "/verify" not in u, timeout=20000)
        ctx.storage_state(path=str(STATE))
    return ctx, page


# ---------------------------------------------------------------------------
# Pages. One function per docs page; the name is the folder under screens/.
# ---------------------------------------------------------------------------

def create_an_agent(s: Stage):
    pg = s.page
    s.go("/agents")
    # The agent's menu and the page next to it, without the test chat.
    panels = pg.locator("div.rounded-2xl[class*='bg-sidebar']")
    main = [panels.filter(has_text="Overview").filter(has_text="Deploy").first,
            pg.locator("div.rounded-2xl.overflow-hidden.min-w-0").first]

    if not CLIPS_ON:
        return create_an_agent_pages(s, remember("agent") or agent_id(pg.url), main)

    # Clip: from the agent switcher to a generated agent.
    s.record()
    s.wait(600)
    switcher = pg.get_by_role("button", name="Switch agent")
    s.click(switcher)
    s.click(pg.get_by_role("menuitem", name="New agent"))
    dialog = pg.get_by_role("dialog")
    s.shot("new-agent.png", dialog, highlight=dialog.get_by_role("button", name="From scratch"), pad=2)
    s.click(dialog.get_by_role("button", name="From scratch"))
    s.type(dialog.locator("textarea"), "Support agent for my clothing store that answers order status, returns and sizing questions, in a warm, short style.")
    s.shot("describe.png", dialog, highlight=dialog.get_by_role("button", name="Generate agent"), pad=2)
    before = agent_id(pg.url)
    s.click(dialog.get_by_role("button", name="Generate agent"), pause=100)
    s.fast(5)
    pg.wait_for_url(lambda u: "/agents/agt_" in u and agent_id(u) != before, timeout=120000)
    pg.wait_for_load_state("networkidle")
    s.fast(1)
    s.wait(1500)
    s.stage()
    s.save_clip()

    create_an_agent_pages(s, remember("agent", agent_id(pg.url)), main)


def create_an_agent_pages(s: Stage, agent: str, main: list):
    pg = s.page
    base = f"/agents/{agent}"

    s.go(base + "/identity")
    s.shot("identity.png", main, pad=8, highlight=pg.get_by_role("link", name="Identity"))

    s.go(base + "/data-sources")
    add = pg.get_by_role("button", name="Add content")
    box = add.bounding_box()
    s.click(add)
    menu = pg.get_by_role("menu")
    mb = menu.bounding_box()
    s.shot("add-content.png", {"x": mb["x"] - 420, "y": box["y"] - 16,
                               "width": box["x"] + box["width"] - mb["x"] + 436,
                               "height": mb["y"] + mb["height"] - box["y"] + 32})
    QUESTION = "Can I return a dress if it doesn't fit?"
    if pg.get_by_text(QUESTION).count():
        pg.keyboard.press("Escape")
    else:
        s.click(menu.get_by_role("menuitem", name="Add Q&A"))
        qa = pg.get_by_role("dialog")
        s.type(qa.get_by_label("Question"), QUESTION, delay=12)
        s.type(qa.get_by_label("Answer"), "Yes. Unworn dresses with tags can be returned within 30 days of delivery "
               "for a full refund or a free exchange for another size. Start a return from your order page "
               "or reply here with your order number.", delay=4)
        s.click(qa.get_by_role("button", name="Add pair"))
    for _ in range(90):  # sources are processed in the background
        if pg.get_by_text("Ready", exact=True).count():
            break
        pg.wait_for_timeout(1000)
        if _ % 10 == 9:
            pg.reload(); s.stage()
    # As it looks with the test chat closed: the table gets the full width.
    pg.evaluate("""() => { for (const el of document.querySelectorAll('div.rounded-2xl'))
        if (el.textContent.includes('Test chat')) el.style.display = 'none'; }""")
    s.wait(600)
    b = main[1].bounding_box()
    s.shot("sources-ready.png", {"x": b["x"] - 8, "y": b["y"] - 8, "width": b["width"] + 16, "height": 250})

    # The test chat panel beside the Identity page, after the agent replies.
    s.go(base + "/identity")
    panel = pg.locator("div.rounded-2xl").filter(has_text="Test chat").last
    s.type(panel.locator("textarea, [contenteditable='true']").last, QUESTION)
    pg.keyboard.press("Enter")
    sent = len(panel.inner_text())
    last, still = "", 0
    for _ in range(90):  # until the reply has arrived and stopped streaming
        pg.wait_for_timeout(1000)
        text = panel.inner_text()
        still = still + 1 if text == last else 0
        last = text
        if len(text) > sent + 60 and still >= 3:
            break
    s.shot("test-chat.png", panel, pad=8)

    s.go(base + "/deploy")
    s.shot("deploy.png", main, pad=8, highlight=pg.get_by_text("Where Fufa replies").locator("xpath=../.."))


PAGES = {"create-an-agent": ("agents/create-an-agent", create_an_agent)}


CLIPS_ON = "--no-clips" not in sys.argv


def main():
    wanted = [a for a in sys.argv[1:] if not a.startswith("--")] or list(PAGES)
    with sync_playwright() as p:
        browser = p.chromium.launch()
        ctx, page = sign_in(browser)
        for key in wanted:
            folder, run = PAGES[key]
            print(key)
            run(Stage(page, folder))
        ctx.storage_state(path=str(STATE))
        browser.close()


if __name__ == "__main__":
    main()
