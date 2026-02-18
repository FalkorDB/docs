# AI-Readable Documentation

This documentation site is designed to be AI-friendly by providing clean markdown versions of all documentation pages.

## Features

### 1. Markdown URL Endpoints

For every documentation page, a markdown version is available by appending `.md` to the URL.

**Examples:**
- HTML: `https://docs.falkordb.com/` → Markdown: `https://docs.falkordb.com/.md`
- HTML: `https://docs.falkordb.com/getting-started/clients` → Markdown: `https://docs.falkordb.com/getting-started/clients.md`
- HTML: `https://docs.falkordb.com/cypher/indexing/vector-index` → Markdown: `https://docs.falkordb.com/cypher/indexing/vector-index.md`

### 2. Clean Markdown Output

The markdown versions are stripped of:
- Navigation menus
- Sidebars
- Footers
- Theme elements
- JavaScript and styling

Only the core documentation content is included, making it optimal for AI tools to parse and understand.

### 3. Content Structure

Each markdown page includes:
- Page title (as H1)
- Page description (if available)
- Main content body

## Implementation Details

### Jekyll Plugin

A custom Jekyll plugin (`_plugins/markdown_generator.rb`) automatically generates `.md` versions of all documentation pages during the build process.

### Clean Layout

The `_layouts/markdown.html` layout renders content without any theme-specific elements, providing clean, focused markdown output.

### Build Process

The site uses a custom GitHub Actions workflow (`.github/workflows/pages.yml`) that:
1. Builds the Jekyll site with custom plugins enabled
2. Generates both HTML and markdown versions
3. Deploys to GitHub Pages

## For AI Tools

AI tools can:
1. Directly request the `.md` version of any page
2. Parse clean markdown without HTML noise
3. Access structured documentation content efficiently

## Note on Content Negotiation

While the Accept header approach (`Accept: text/markdown`) would be ideal, GitHub Pages' static hosting doesn't support server-side content negotiation. The `.md` URL suffix provides a reliable alternative that works with all clients.
