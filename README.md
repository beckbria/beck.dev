# Hugo Static Site with Docker & Congo Theme

A fully containerized setup for initializing, developing, and building a static blog using [Hugo](https://gohugo.io/) and the premium [Congo](https://github.com/jpanther/congo) theme.

## Features

- **Zero Local Dependencies:** Only requires Docker and Docker Compose. No local installation of Hugo or Go is necessary.
- **Hugo Extended (v0.128.2):** Built with Hugo Extended which supports Sass/SCSS compilation (required by Congo).
- **Hugo Modules:** Uses modern Hugo Modules to manage themes, enabling easy theme updates.
- **Host Output (Extraction):** Built files are compiled directly into the `./public` folder on your host machine for simple deployment.

---

## Getting Started

### Prerequisites

- **Docker Desktop** installed and running on your system.

### Running the Site Locally (Development Mode)

To spin up the Hugo development server with live reloading enabled:

#### Windows (PowerShell)
```powershell
.\run.ps1 dev
```

#### WSL / macOS / Linux / Git Bash
```bash
chmod +x run.sh  # Ensure executable permission
./run.sh dev
```

The site will be built and served locally. Open your browser and navigate to:
👉 **[http://localhost:1313/](http://localhost:1313/)**

*Live reload is enabled by default—any edits you make to content or styling will immediately update in your browser.*

---

## Production Build & File Extraction

To compile your site and generate optimized static files for deployment to a web server (e.g. Netlify, Vercel, Nginx, Apache):

#### Windows (PowerShell)
```powershell
.\run.ps1 build
```

#### WSL / macOS / Linux / Git Bash
```bash
./run.sh build
```

This runs the Hugo compiler (`hugo --gc --minify`) inside the Docker container. 
The generated static site files will be outputted directly to the **`./public/`** folder in your project's root directory on your host machine. You can copy the contents of this folder directly to your hosting provider or server.

---

## Other Actions

### Cleaning Up Build Output
To delete the generated `./public/` and `./resources/` folders:
```powershell
.\run.ps1 clean   # Windows (PowerShell)
./run.sh clean     # WSL / Linux / macOS
```

### Accessing the Container Shell
If you need to run custom Hugo commands (e.g. `hugo new posts/my-new-post.md`), you can enter the container's interactive bash shell:
```powershell
.\run.ps1 shell   # Windows (PowerShell)
./run.sh shell     # WSL / Linux / macOS
```

---

## Directory Structure

```text
├── config/
│   └── _default/
│       ├── hugo.toml     # Global Hugo settings
│       ├── markup.toml   # Markdown parsing config (e.g., enable HTML)
│       ├── menus.toml    # Header and footer navigation menus
│       └── params.toml   # Theme configuration (colors, author bio, social links)
├── content/
│   ├── _index.md         # Home page content
│   └── posts/
│       └── my-first-post.md # Sample post file
├── Dockerfile            # Container image definition with Hugo Extended & Go
├── docker-compose.yml    # Development environment orchestration
├── go.mod                # Module definition (for theme modules)
├── run.ps1               # PowerShell helper script
├── run.sh                # Shell helper script
└── README.md             # This documentation
```
