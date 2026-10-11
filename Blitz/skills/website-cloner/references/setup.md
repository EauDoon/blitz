# Target Project Setup

The clone needs somewhere to land. Two routes. Commands below work in bash and in PowerShell except the folder step, which has one line for each shell.

## Route A: from the template repo (fastest)

The upstream template ships the scaffold already configured: Next.js 16, React 19, Tailwind v4, shadcn/ui, TypeScript strict, plus the `docs/` and `public/` folder structure this pipeline expects.

Do not clone the repo directly; it is a GitHub *template*. Either use the **Use this template** button on GitHub to create a fresh repo, or take the tree without its git history:

```powershell
npx degit JCodesMore/ai-website-cloner-template <project-name>
cd <project-name>
git init
npm install
npm run build
```

`degit` copies the working tree with no history, which is what you want: the clone project should own its first commit. Node 24+ is required.

## Route B: scaffold from scratch

When the owner wants a different stack, or a clone dropped into an existing project.

```powershell
npx create-next-app@latest <project-name> --typescript --tailwind --app --src-dir --import-alias "@/*"
cd <project-name>
npx shadcn@latest init
git init
```

Then create the folders this pipeline writes into:

```bash
mkdir -p docs/research/components docs/design-references public/images public/videos public/seo src/types scripts
```

On Windows PowerShell:

```powershell
mkdir docs\research\components, docs\design-references, public\images, public\videos, public\seo, src\types, scripts -Force
```

Confirm `npm run build` passes before extracting anything.

## Serving the clone for QA

Phase 5 compares the clone against the original side by side. Give the Browser pane a way to start the dev server by creating `.claude/launch.json`:

```json
{
  "version": "0.0.1",
  "configurations": [
    {
      "name": "clone",
      "runtimeExecutable": "npm",
      "runtimeArgs": ["run", "dev"],
      "port": 3000
    }
  ]
}
```

Then `preview_start {name: "clone"}` for the clone and `preview_start {url}` or `tabs_create` + `navigate` for the original. Two tabs, switch with `tabs_select`. Never start the dev server through Bash.

## Git and worktrees

`git init` matters. Builder agents launched with `isolation: "worktree"` need a git repo, and the whole point of the incremental pipeline is a verified build at each merge.

Commit after the foundation phase lands, then after each section merges. If a builder's worktree comes back unchanged it is cleaned up automatically.

Worktrees are only worth their setup cost when builders touch shared files. When each builder creates one new component file of its own, run them in parallel in place and skip the isolation overhead.

## Windows notes, when the rig is Windows

- `npm` and `npx` work normally under PowerShell. Bash-isms from upstream docs (`&&` chains, `mkdir -p`) do not; use `;` with `if ($?)`, or `New-Item -ItemType Directory -Force`.
- The upstream repo's `scripts/sync-agent-rules.sh` is a maintenance script for the template itself. Irrelevant here.
- Long asset paths under `public/` can hit the Windows path limit on deeply nested CDN structures. Flatten the download directory rather than mirroring the source URL path exactly.
