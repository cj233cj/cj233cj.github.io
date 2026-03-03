# Personal Blog

A static blog built with Python Pelican, styled with the Papyrus theme, and automatically deployed to GitHub Pages.

## Tech Stack

- **Static Site Generator**: [Pelican](https://getpelican.com/)
- **Theme**: [Papyrus](https://github.com/aleylara/Papyrus)
- **Python Environment**: [uv](https://github.com/astral-sh/uv)
- **Deployment**: GitHub Actions → GitHub Pages

## Live Site

🌐 [https://cj233cj.github.io/](https://cj233cj.github.io/)

## Deployment

The site automatically deploys to GitHub Pages via GitHub Actions on every push to the `master` branch.


## Project Structure
```
.
├── content/           # Blog posts and pages
├── themes/
│   └── Papyrus/      # Theme files
├── pelicanconf.py    # Development configuration
├── publishconf.py    # Production configuration
├── pyproject.toml    # Python dependencies
└── .github/
    └── workflows/
        └── deploy.yml # GitHub Actions workflow
```

## Configuration

- **Development**: Edit `pelicanconf.py`
- **Production**: Edit `publishconf.py`
- **Theme settings**: Customize in `pelicanconf.py`

## Caveat

blog articles may or may not contain some AI slop, currently it's mostly for practice english/japanese writing under the vetting of AI 

## Todo

- [ ]  google analysis or something 
- [ ]  hehe
- [ ]  music player 
- [ ]  cjk fonts and de-google
- [ ]  ...