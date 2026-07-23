# Team Snapdragons - FastAPI Service

<img width="1707" height="400" alt="snapdragons-banner" src="https://github.com/user-attachments/assets/d0f5f5ca-39f6-4ddb-b75b-0c0e5a3a0da6" />

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

Run Server with:

```
fastapi dev src/main.py
```

Run Frontend with:

```
streamlit run app.py
```