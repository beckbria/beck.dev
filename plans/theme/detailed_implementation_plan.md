# Detailed Implementation Plan: Custom Theme

This document details the specific files that will be created or modified to build the custom Hugo theme for beck.dev. It also outlines the updates to the `README.md` documentation for content management.

## 1. Configuration & Theme Setup
*   **`config/_default/hugo.toml`**: Update the `theme` property to point to the new custom theme (e.g., `theme = "beck"`).
*   **`themes/beck/theme.toml`**: Create the theme metadata file.

## 2. Layouts & Templates (`themes/beck/layouts/`)
*   **`_default/baseof.html`**: The master HTML skeleton containing the `<html>`, `<head>`, and `<body>` tags.
*   **`partials/head.html`**: Meta tags, SEO, and CSS/JS asset inclusion.
*   **`partials/header.html`**: Site navigation menu.
*   **`partials/footer.html`**: Footer content and links.
*   **`index.html`**: Home page template (bio, recent photos, recent blog posts). *Note: Will use a placeholder image for the biography picture initially, to be replaced later.*
*   **`_default/list.html`**: Default list template for blog posts with category filters.
*   **`_default/single.html`**: Default single page for rendering individual markdown posts.
*   **`photos/list.html`**: Custom layout for the CSS Grid photo gallery.
*   **`photos/single.html`**: Custom detail view for a specific photo.
*   **`travel/list.html`**: Dedicated page for the interactive Leaflet.js map.

## 3. Assets (`themes/beck/assets/`)
*   **`css/main.css`**: Core styling, defining the "Hybrid/Balanced" design using custom CSS (or Tailwind CSS if adopted).
*   **`js/map.js`**: JavaScript logic for initializing Leaflet.js on the travel page.
*   **`images/placeholder-bio.jpg`**: Placeholder image for the home page biography.

## 4. Content Adjustments
*   **`content/_index.md`**: Update front matter to reference the placeholder biography image.
*   **`content/travel/_index.md`**: Setup for the Leaflet map page.
*   **`content/photos/_index.md`**: Setup for the photos page.

---

## README.md Updates

The `README.md` will be updated to include the following content management instructions:

### Managing Content

#### Adding a New Blog Post
To add a new blog post, create a markdown file in `content/posts/` (or `content/blog/`).
You can use the provided container shell:
```bash
./run.sh shell
hugo new posts/my-new-post.md
```
**Visibility Control:** In the generated markdown file's front matter, set `draft: true` to keep the post hidden. Change it to `draft: false` when you are ready to publish it publicly.

#### Adding a New Photo
Photos use Hugo page bundles to bind high-resolution images and metadata together.
1. Create a new folder for the photo (e.g., `content/photos/my-new-photo/`).
2. Drop your full-resolution image into this folder (e.g., `image.jpg`).
3. Create an `index.md` file in the folder to hold your tags, location, and text description.
**Visibility Control:** Set `draft: true` in the `index.md` front matter to hide the photo from the gallery. Set `draft: false` to publish it. (The theme will automatically handle responsive resizing).

#### Adding a New Location Travelled
Locations on the interactive map are driven by content entries.
1. Create a new entry under the travel section (e.g., `content/travel/yosemite.md`).
2. Include geographic coordinates (`latitude` and `longitude`) in the front matter.
**Visibility Control:** Set `draft: true` in the front matter to hide this location marker from the public map. Set `draft: false` to display it.
