# CLAUDE.md

Hugo personal blog (source for cj233cj.github.io). Branch `test` is the working branch; `master` is what ships.

## Layout
- `content/` — posts and pages
- `layouts/` + `assets/` — theme customization (templates, CSS/JS)
- `themes/` — third-party theme(s)
- `hugo.toml` — site config
- `static/` — raw files copied to the site as-is

## Rules
- `public/` is generated Hugo output used for local preview only. **Never edit it, never include it in diffs you discuss, never clean it up.**
- Build locally with `hugo` (add `-D` to include drafts). To preview: `hugo server -D`.
- Changes to appearance come from `layouts/`/`assets/`, not from files in `public/`.

- Preserve the existing theme's design language unless explicitly asked otherwise.
- Prefer minimal changes over rewriting existing templates.
- Do not introduce JavaScript unless necessary.
- Keep CSS simple and maintainable.
- Use Hugo idioms and template functions.
- Check Hugo template syntax after modifications.
- Do not modify unrelated files.
- Before committing, inspect `git diff`.
- Never commit unless explicitly asked.
- mostly you only work with theme files and don't touch blog content 