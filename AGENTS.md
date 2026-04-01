# Repository instructions for AI agents

This repository is a **Hugo** site (`42jerrykim.github.io`). Agents editing content should follow project rules and skills under `.cursor/`.

## Always respect

- **`.cursor/rules/rules-that-must-be-followed.mdc`** (always applied): new posts use `draft: true` until review; tags ≥50 with English and Korean; description ~150 characters; title ≤70 characters; confirm dates via terminal (e.g. PowerShell `Get-Date -Format "yyyy-MM-dd"`); verify every external link with HTTP before adding or keeping; Mermaid node IDs and quoting rules as specified there.
- **Algorithm posts**: include the required comment at the top of solution code blocks (see the same rules file).

## Content layout

- **Regular posts**: `content/post/<year>/<YYYY-MM-DD-slug>/index.md`
- **Collection posts**: `content/collection/<collection>/<year>/<folder>/index.md`
- **Tags**: prefer entries from `data/tags.yaml`.

## When writing or refactoring posts

1. Read **`.cursor/skills/blog-post-writing/SKILL.md`** and **`reference.md`** (same folder) for paths, front matter, internal links, and title prefixes.
2. If the task is a full pipeline (research → draft → QA), use **`.cursor/skills/blog-agent-pipeline/SKILL.md`** and run its stages in order.
3. For collection-specific structure (Movies, TV-Show, Vocabulary, Algorithm, bashshell, cmd), follow the matching **`.cursor/rules/*.mdc`** under that collection in `content/collection/`. Those rules declare **`globs`** (e.g. `content/collection/Movies/**/*.md`) so Cursor includes them when you edit matching markdown files; if a task spans paths outside that glob, still **@mention** the rule or open a file under the glob so context applies.
4. For long educational series (e.g. optimization tracks), also follow **`.cursor/skills/educational-content-writing/SKILL.md`** when applicable.
5. For movie reviews, also follow **`.cursor/skills/movie-review-writing/SKILL.md`**.

## Internal links

- When editing collection index pages, follow **`.cursor/rules/hugo-collection-internal-links.mdc`** and `blog-post-writing/reference.md` (Hugo collection internal links section).

## Batch CLI (optional)

- `script/md-improve/generate-improve-commands.ps1` can emit `agent -p` lines for bulk markdown improvements; not required for normal IDE editing.
