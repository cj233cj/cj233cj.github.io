# Personal Blog

A static blog built with Python Pelican, styled with the Papyrus theme, and automatically deployed to GitHub Pages.

## Tech Stack

- **Static Site Generator**: [Pelican](https://getpelican.com/)
- **Theme**: [Papyrus](https://github.com/aleylara/Papyrus)
- **Python Environment**: [uv](https://github.com/astral-sh/uv)
- **Deployment**: GitHub Actions → GitHub Pages

## Live Site

🌐 [https://cj233cj.github.io/](https://cj233cj.github.io/)

## Local Development

### Prerequisites

- Python 3.12+
- uv package manager

### Setup
```bash
# Install uv if you haven't already
curl -LsSf https://astral.sh/uv/install.sh | sh

# Clone the repository
git clone https://github.com/cj233cj/cj233cj.github.io.git
cd cj233cj.github.io

# Install dependencies
uv sync

# Start development server
uv run pelican --listen
```

Visit `http://localhost:8000` to preview your blog locally.

## Creating Content

Create new posts in the `content/` directory:
```markdown
Title: My New Post
Date: 2025-12-19
Category: Blog
Tags: python, pelican

Your content here...
```

## Building for Production
```bash
# Generate static files
uv run pelican content -s publishconf.py
```

The output will be in the `output/` directory.

## Deployment

The site automatically deploys to GitHub Pages via GitHub Actions on every push to the `master` branch.

### Workflow

1. Push changes to `master`
2. GitHub Actions builds the site with Pelican
3. Generated files are deployed to GitHub Pages
4. Site updates at https://cj233cj.github.io/

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

## License

This blog is mostly AI slop and for fun