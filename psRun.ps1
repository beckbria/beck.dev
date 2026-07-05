param (
    [string]$Action
)

$ValidActions = @("dev", "build", "clean", "shell")

if ($null -eq $Action -or $Action -eq "" -or $ValidActions -notcontains $Action) {
    Write-Host "Usage: .\run.ps1 <action>" -ForegroundColor Yellow
    Write-Host "Available actions:"
    Write-Host "  dev     - Start local development server at http://localhost:1313"
    Write-Host "  build   - Compile static site to public/ directory"
    Write-Host "  clean   - Remove generated public/ and resources/ files"
    Write-Host "  shell   - Open an interactive shell inside the Hugo container"
    exit 1
}

switch ($Action) {
    "dev" {
        Write-Host "Starting local development server..." -ForegroundColor Green
        docker compose up
    }
    "build" {
        Write-Host "Building static site (extracting to ./public)..." -ForegroundColor Green
        docker compose run --rm hugo hugo --gc --minify
    }
    "clean" {
        Write-Host "Cleaning up build directories..." -ForegroundColor Green
        if (Test-Path -Path "./public") {
            Remove-Item -Path "./public" -Recurse -Force
            Write-Host "Removed public/"
        }
        if (Test-Path -Path "./resources") {
            Remove-Item -Path "./resources" -Recurse -Force
            Write-Host "Removed resources/"
        }
        Write-Host "Clean finished." -ForegroundColor Green
    }
    "shell" {
        Write-Host "Entering container shell..." -ForegroundColor Green
        docker compose run --rm --entrypoint bash hugo
    }
}
