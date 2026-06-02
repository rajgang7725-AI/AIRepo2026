# Developer Setup (Local) — WorkSync MVP

This document explains how to set up a local development environment for the WorkSync MVP.

Prerequisites
- Python 3.10+ installed and on PATH
- Git
- (Windows) PowerShell is available

Quick start (PowerShell)

```powershell
# from project root
.\scripts\setup_dev.ps1
# then
.\.venv\Scripts\Activate.ps1
python manage.py runserver
```

What the script does
- Creates a `.venv` virtual environment
- Installs packages from `requirements.txt`
- Initializes a Django project named `worksync` if not already present
- Runs `python manage.py migrate` to create SQLite schema

Environment variables
- Copy `.env.example` to `.env.local` and edit `SECRET_KEY` and other values as needed.

Manual steps (alternative)

```bash
python -m venv .venv
source .venv/bin/activate  # or `.venv\Scripts\Activate.ps1` on Windows
pip install -r requirements.txt
django-admin startproject worksync .  # only if project not created
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Notes
- `settings.DEFAULT_WEEKLY_HOURS` should be added to the Django settings once the project is created (Sprint 0 artifact).
- For local development we use SQLite as configured by default.
