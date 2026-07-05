# Personal Website Implementation Plan (beck.dev)

This plan outlines the design, architecture, and structural approach for your static personal website at `beck.dev`.

## Approved Design Decisions

*   **Visual Layout**: Hybrid / Balanced. A middle ground with a compact bio, immediate access to recent photo thumbnails, and a clean list of blog posts.
*   **Tag Architecture**: Separate tags pages (`/blog/tags/` and `/photos/tags/`). This provides clean, contextual filtering so readers only see tags relevant to the medium they are currently viewing.
*   **Content Separation**: One unified chronological feed on the home page / blog list. Strong visual signifiers (category filters and distinct icons for SWE, Photography, and Maker) will be used to easily isolate topics.

## Proposed Technical Architecture

Given the strict requirement for a completely static site (no PHP/DB) with high performance and accessibility, we will proceed with **Hugo** as the static site generator.

### Theme Strategy: Existing vs. Custom

*   **Tweaking an existing theme (e.g., Congo)**: While popular themes like Congo are excellent out-of-the-box for standard blogs, achieving the specific "Hybrid" layout with custom thumbnail grids, bespoke category filters, and a dedicated Leaflet map page would require overriding a significant number of core templates (`layouts/index.html`, list pages, etc.). 
*   **Creating a Custom Theme**: 
    *   *Recommendation*: **Create a custom theme**. Since the design requirements are clear and highly specific, building a custom theme from scratch using standard CSS or Tailwind CSS is highly recommended. This ensures you aren't fighting a parent theme's assumptions, results in a much smaller footprint (faster load times), and makes long-term maintenance significantly easier.

### Content Management & Photo Workflow
Markdown files with YAML/TOML front matter for Blog posts and Projects. Photos will use page bundles to bind metadata (location, Exif data, text descriptions) to the image files.

**Workflow for Adding a New Photo**:
Hugo natively supports automatic image processing at build time. You do **not** need to manually resize images or run scripts. 
1. **Drop the Full-Res Image**: Place the full-resolution photo into a new page bundle folder (e.g., `content/photos/my-new-photo/image.jpg`).
2. **Add Metadata**: Create an `index.md` file in that folder with your tags, location, and description.
3. **Automatic Resizing**: When you run `hugo` (or `hugo server`), the custom theme will automatically generate responsive thumbnails for the homepage and photo grid using Hugo's native `Resize` and `Fit` functions. Hugo aggressively caches these generated images in the `resources` directory, so subsequent builds remain incredibly fast.

### Routing & URLs
*   `/` - Home page with bio, recent photo thumbnails, and recent blog posts.
*   `/blog/` - Paginated list with category filters.
*   `/blog/my-post-title/` - Slugified URLs based on front matter title.
*   `/photos/` - CSS Grid gallery of thumbnails.
*   `/photos/yosemite-trip-2024/` - Detail view with direct linkability.
*   `/travel/` - Dedicated interactive Leaflet.js map. Map markers will link directly to contextual photo tag pages (e.g., `/photos/tags/san-francisco/`).
*   `/projects/` - Grid or list of cards with GitHub and Live URLs.

## Verification Plan

### Automated Checks
*   Run Lighthouse audits locally to ensure 95+ scores in Performance, Accessibility, and SEO.
*   Verify HTML structure using automated accessibility checkers (e.g., axe-core).

### Manual Verification
*   Test keyboard navigation (Tab through all links, ensure focus states are highly visible).
*   Test contrast ratios using color contrast tools.
*   Verify all layout breakpoints (mobile, tablet, desktop).
*   Verify map markers successfully route to the correct photo tag URLs.
