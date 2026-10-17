# Writing Fufa docs

Rules for anyone adding a page, person or AI. The site is read by customers and by answer engines and coding agents, so every page has the same shape.

## Where a page goes

The sidebar follows a new customer through the product. One folder per group under `src/content/docs/`:

| Folder | Group | What belongs here |
| --- | --- | --- |
| `start/` | Start | Create a workspace, a one-page tour of the inbox. The only overview pages. |
| `channels/` | Channels | One page per channel a customer can turn on today. |
| `inbox/` | Inbox | Reply, assign, status, team hours and handover, canned responses. |
| `contacts/` | Contacts | Contacts, tags, attributes, segments. |
| `campaigns/` | Campaigns | Send a campaign, WhatsApp templates, the opt-in popup. |
| `agents/` | Agents | Create, knowledge, actions and connectors, test, deploy, voice. |
| `workflows/` | Workflows | How a run moves, then only triggers and actions a customer sets up alone. |
| `commerce/` | Commerce | Shopify, catalog, orders, abandoned carts. |
| `workspace/` | Workspace | Team and roles, billing and credits, workspace settings. |

A page shows up in the sidebar because its file exists. Set its position with `sidebar.order` in the frontmatter. A group with no pages stays hidden. When you add the first page to an empty group, restart `pnpm dev` so the group appears.

Don't document a feature before customers can use it. Messenger stays out until it ships.

## Page shape

Pages are plain `.md`, never `.mdx`, so the markdown copy at `<url>.md` and `/llms-full.txt` read cleanly.

```md
---
title: Connect WhatsApp            # the task, as an imperative
description: One sentence stating the result the reader gets. 120 to 160 characters.
sidebar:
  order: 1
---

First paragraph: the result, in plain words. What the reader has when they finish.

## Before you start
- Role needed (Owner, Admin, Supervisor or Agent) and anything to have ready.

## <Task verb phrase>
1. Numbered steps. UI labels in **bold**, written exactly as the app shows them.

## Check it works
How to see it working.

## Common questions
### A question a customer would type into a search box?
A direct answer in the first sentence, then detail.

## Related
- Links to the next tasks.
```

- **Common questions** becomes FAQ structured data automatically (see `src/route-data.ts`). Keep each answer self-contained, because it may be quoted alone.
- Prefer slugs that name the thing (`channels/whatsapp`, `workspace/team`), so a title can change without breaking links. Use a short action slug only when there's no clear noun (`start/create-a-workspace`). Never rename a published slug.
- Link with absolute paths and a trailing slash: `[Connect WhatsApp](/channels/whatsapp/)`.
- Asides use `:::note`, `:::tip` or `:::caution` blocks, sparingly.

## How the design picks up a page

`src/styles/design.css` styles the fixed sections by their headings, so the markdown stays plain:

- **Before you start**: the bullet list right after it becomes a checklist card.
- Every numbered list becomes numbered steps.
- **Common questions**: each `###` question and the single paragraph after it becomes a Q&A card. Keep each answer to one paragraph.
- **Related**: each bullet must be only a link, which becomes a chip.
- The group eyebrow and icon above the title come from the folder (`src/components/PageTitle.astro`, icons in `GroupIcon.astro`).

Keep these heading names exactly as written, or the styling and the FAQ data won't apply.

## Check UI labels against the app

Before writing a step, find the label in `apps/web` in the monorepo and copy it exactly. Permissions come from `packages/shared/src/core/permissions.ts`. Don't describe behaviour you haven't found in the code or seen in the app.

## What the build publishes for machines

- `/llms.txt`, `/llms-full.txt`, `/llms-small.txt`, plus the sets in `astro.config.mjs`, from `starlight-llms-txt`.
- `<page>.md`: each page as markdown, from `src/pages/[...slug].md.ts`.
- JSON-LD on every page (TechArticle, BreadcrumbList, and FAQPage when the page has questions), from `src/route-data.ts`.
- `robots.txt` that welcomes AI crawlers, and `sitemap-index.xml`.
