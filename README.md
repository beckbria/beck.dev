# Personal Website

This is the code for [my personal website](https://beck.dev). The site is entirely static, generated with [Hugo](https://gohugo.io/).

---

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
.\run.ps1 dev
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
.\run.ps1 build
```
The generated site will be output to the **`./public/`** folder in your project's root directory.

---

## Other Actions

### Cleaning Up Build Output
To delete the generated `./public/` and `./resources/` folders:

#### WSL / Linux
```bash
./run.sh clean
```

#### Windows
```powershell
.\run.ps1 clean
```

### Accessing the Container Shell
If you need to run custom Hugo commands (e.g. `hugo new posts/my-new-post.md`), you can enter the container's interactive bash shell:

#### WSL / Linux
```bash
./run.sh shell
```

#### Windows
```powershell
.\run.ps1 shell
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
