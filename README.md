# Team Snapdragons - FastAPI Service

[![Tests](https://github.com/bverble-catalyte/snapdragons-fastapi-service/actions/workflows/tests.yml/badge.svg)](https://github.com/bverble-catalyte/snapdragons-fastapi-service/actions/workflows/tests.yml)

This is the Team Snapdragons FastAPI service.

## Contributing

Ensure Python is installed. Then:

```
git clone git@github.com:bverble-catalyte/snapdragons-fastapi-service.git
cd snapdragons-fastapi-service
```

Create a virtual environment:

```
# bash
python -m venv .venv
source .venv/bin/activate

# PowerShell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

Install dependencies:

```
pip install -r requirements.txt
```

Run with:

```
fastapi dev src/main.py
```
