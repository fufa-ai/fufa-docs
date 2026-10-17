# Fufa docs

Public documentation for [Fufa](https://fufa.ai), built with [Starlight](https://starlight.astro.build/).

Pages live in `src/content/docs`. The build writes the site plus `/llms.txt`, `/llms-full.txt`, and `/llms-small.txt` from those pages.

This repo is meant to be public. It is vendored into the private Fufa monorepo as the `apps/docs` submodule. The remote is not attached yet.

## Commands

From this directory:

```bash
pnpm install
pnpm dev
pnpm build
```

`pnpm dev` serves the site at `http://localhost:4321`.

## Attach the public remote

Create the empty public repository, then from this directory:

```bash
git remote add origin git@github.com:fufa-ai/fufa-docs.git
git push -u origin main
```

If the repository URL is different, update it from the monorepo root as well:

```bash
git submodule set-url apps/docs <public-repo-url>
```

Push this repository before pushing the monorepo branch that records the submodule.
