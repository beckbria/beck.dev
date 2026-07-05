# Personal Website

This is the code for [my personal website](https://beck.dev). The site is entirely static, generated with [Hugo](https://gohugo.io/).

## Development

### Prerequisites

* Install [Docker Engine](https://docs.docker.com/engine/install/)
* (Optional, **highly recommended**): [Configure Docker to run rootless](https://docs.docker.com/engine/security/rootless/)

### Running the Site Locally (Development Mode)

#### WSL / Linux
```bash
./run.sh dev
```

#### Windows
```powershell
.\psRun.ps1 dev
```

The site will be built and served locally at **[http://localhost:1313/](http://localhost:1313/)**

---

## Production Build & File Extraction

#### WSL / Linux
```bash
./run.sh build
```

#### Windows
```powershell
.\psRun.ps1 build
```
The generated site will be output to the **`./public/`** folder in your project's root directory.

---

## Other Actions

### Accessing the Container Shell
If you need to run custom Hugo commands (e.g. `hugo new posts/my-new-post.md`), you can enter the container's interactive bash shell:

#### WSL / Linux
```bash
./run.sh shell
```

#### Windows
```powershell
.\psRun.ps1 shell
```
### Cleaning Up Build Output
To delete the generated `./public/` and `./resources/` folders:

#### WSL / Linux
```bash
./run.sh clean
```

#### Windows
```powershell
.\psRun.ps1 clean
```

## Managing Content

### Adding a New Blog Post
To add a new blog post, create a markdown file in `content/posts/`.
You can use the provided container shell:
```bash
./run.sh shell
hugo new posts/my-new-post.md
```
**Visibility Control:** In the generated markdown file's front matter, set `draft: true` to keep the post hidden. Change it to `draft: false` when you are ready to publish it publicly.

### Adding a New Photo

You can add photos automatically using the helper script or manually.

#### Automated Import (Recommended)
Run the import script in WSL, passing either a file path or a directory containing `*.jpg`/`*.jpeg` images:
```bash
# Import a single image
./add_photo.sh /path/to/my-new-photo.jpg

# Batch import all JPGs in a directory
./add_photo.sh /path/to/my-photos-directory/
```
This script will:
1. Create a new folder under `content/photos/` for each image.
2. Extract the photo's original date from EXIF data (`DateTimeOriginal`) if available, or fall back to the file's creation date.
3. Create `index.md` inside each folder with the required metadata and tags.
4. Move the photo file into the folder.
5. Scrub sensitive EXIF metadata (Camera Serial Number, Lens Serial Number, GPS info, original filename, software name, and artist name) from the imported images.


After running the script, you should manually edit `index.md` to provide a title, description, and appropriate tags

#### Cleaning Metadata in Bulk
If you have manually imported photos or want to ensure that all images in your gallery are thoroughly cleaned of sensitive metadata, you can run the bulk cleaning utility in WSL:
```bash
./clean_exif.sh
```
This script recursively scans `content/photos/` and strips the same list of sensitive EXIF fields (Serial Number, Lens Serial Number, GPS, Software, Artist, and Filename) in place.

#### Manual Import
1. Create a new folder for the photo (e.g., `content/photos/my-new-photo/`).
2. Drop your full-resolution image into this folder (e.g., `image.jpg`).
3. Create an `index.md` file in the folder to hold your tags, location, and text description.

**Visibility Control:** Set `draft: true` in the `index.md` front matter to hide the photo from the gallery. Set `draft: false` to publish it. (The theme will automatically handle responsive resizing).


### Adding a New Location Travelled
Locations on the interactive map are driven by content entries.
1. Create a new entry under the travel section (e.g., `content/travel/yosemite.md`).
2. Include geographic coordinates (`latitude` and `longitude`) in the front matter.
**Visibility Control:** Set `draft: true` in the front matter to hide this location marker from the public map. Set `draft: false` to display it.

## Directory Structure

```text
├── config/
│   └── _default/
│       ├── hugo.toml     # Global Hugo settings
│       ├── markup.toml   # Markdown parsing config (e.g., enable HTML)
│       └── params.toml   # Author parameters
├── content/
│   ├── _index.md         # Home page content (including Bio)
│   ├── photos/           # Photo page bundles
│   ├── posts/            # Blog posts
│   └── travel/           # Travel location pages
├── themes/
│   └── beck/             # Custom 'beck' theme files (layouts, styles, assets)
├── Dockerfile            # Container image definition with Hugo Extended & Go
├── docker-compose.yml    # Development environment orchestration
├── run.ps1               # PowerShell helper script
├── run.sh                # Shell helper script
└── README.md             # This documentation
```
