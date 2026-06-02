# PowerShell script to bootstrap local development environment for WorkSync MVP
# Usage: Open PowerShell, run: .\scripts\setup_dev.ps1

Set-StrictMode -Version Latest

# Create virtual environment
if (-not (Test-Path .\.venv)) {
    python -m venv .venv
}

# Activate venv for current session
Write-Host "Activating virtual environment"
. .\.venv\Scripts\Activate.ps1

# Upgrade pip and install requirements
python -m pip install --upgrade pip
pip install -r requirements.txt

# Optionally initialize Django project if not created
if (-not (Test-Path "worksync\manage.py")) {
    Write-Host "Initializing Django project 'worksync'"
    django-admin startproject worksync .
}

# Run migrations
python manage.py migrate

Write-Host "Setup complete. To run the dev server:"
Write-Host "    .\\.venv\\Scripts\\Activate.ps1"
Write-Host "    python manage.py runserver"
