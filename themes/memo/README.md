# memo

Minimal Hugo theme for Project Digitalsheep. Dark mode toggle. CJK-ready. Old-Twitter card layout.

---

## Features

- Dark mode toggle (remembers preference via localStorage) + auto from system
- Minimal JS — one small inline script for the dark mode toggle only
- CJK-friendly system serif fonts (Japanese/Chinese/English)
- Tweet-style post cards with tags, category, author, date
- Fallback title `#memo` when no title is set
- Fallback summary from article body (~80 chars, CJK-safe)
- `posts` / `archive` / `about` navigation
- Pagination on posts list
- Archive page grouped by year → month with post counts
- Clean about page (no post metadata)
- Custom 404 page
- Mobile friendly

---

## Content front matter

```yaml
---
title: "후현대주의 광장무"
date: 2022-12-12
tags: ["bullshit", "政治哲学"]
category: "道"
author: "フグ"
summary: "街頭政治の生理的要因"
---
```

All fields optional except `date`.

- If `title` is absent → card shows `#memo`
- If `summary` is absent → first ~120 chars of body used

---

## Adding images in articles

Place images in your `content/` folder next to the markdown file, or in `static/`.

**Next to the post (page bundle):**

Rename your post from `post.md` to a folder:
```
content/posts/my-post/
  index.md       ← your markdown
  photo.jpg      ← image lives here
```

Then reference it in markdown:
```markdown
![alt text](photo.jpg)
```

**From static folder:**

Put the image in `static/img/photo.jpg`, then:
```markdown
![alt text](/img/photo.jpg)
```

**External image:**
```markdown
![alt text](https://example.com/photo.jpg)
```

**With caption (HTML, works because unsafe = true):**
```html
<figure>
  <img src="photo.jpg" alt="description" />
  <figcaption>your caption here</figcaption>
</figure>
```

Images in post body are styled `max-width: 100%` and block-displayed automatically.

---

## Directory structure

```
content/
  posts/        ← markdown files (or page bundles with images)
  archive/
    _index.md   ← empty, just needs to exist
  about/
    _index.md   ← your about page content
```

Theme layouts included:
```
layouts/
  _default/
    baseof.html, list.html, single.html
  archive/
    list.html   ← year → month grouped archive
  about/
    single.html ← clean about page, no post metadata
  partials/
    nav.html, post-card.html, pagination.html
  404.html
  index.html    ← redirects to /posts/
```

---

## Install

```
themes/
  memo/         ← this theme folder
```

In `hugo.toml`:
```toml
theme = "memo"
```
