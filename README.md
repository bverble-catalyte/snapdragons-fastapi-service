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

```bash
python -m venv .venv
```

**bash**

```bash
source .venv/bin/activate
```

**PowerShell**

```PowerShell
.venv\Scripts\Activate.ps1
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

Run tests with:

```
pytest
```

## Endpoints

This project contains a `postman.json` file which can be imported into Postman to try out the routes. Ensure the server is running before sending requests.

### Summary

| Method | Path | Description |
| --- | --- | --- |
| `GET` | `/products` | List products
| `GET` | `/products/{id}` | View product
| `GET` | `/products/search` | Search products by name or stock keeping unit
| `POST` | `/products` | Create product

### `GET /products`

List all products.

#### Response Body (JSON)

Returns an array of `Product` objects.

#### Response Codes:

- **200 OK:** On success

### `GET /products/{id}`

View product with identifier `id`.

#### Response Body (JSON)

Returns a `Product` object.

#### Response Codes:

- **200 OK:** On success
- **404 Not Found:** If no such product exists

### `GET /products/search`

Search for products by name or stock keeping unit.

#### Query Params

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | yes | Search for products by name |
| `unit` | string | no | Search for products inventoried by stock keeping unit |

#### Response Body (JSON)

Returns an array of `Product` objects.

#### Response Codes:

- **200 OK:** On success
- **422 Unprocessable Content:** If any required fields are missing or invalid

### `POST /products`

Create a product.

#### Request Body (JSON)

A `ProductCreate` object.

#### Response Body (JSON)

Returns the created `Product` object.

#### Response Codes:

- **201 Created:** On success
- **422 Unprocessable Content:** If any required fields are missing or invalid

### JSON Schemas

#### Product

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | int | yes | The product's unique identifier |
| `name` | string | yes | The product name |
| `unit` | string | yes | The product's unit of sale (e.g. "each", "bag", "lb") |
| `cost_per_unit` | string | yes | Amount the garden center pays suppliers, in dollars per unit |
| `price_per_unit` | string | yes | Amount the garden center charges customers, in dollars per unit |
| `quantity_in_stock` | string | yes | Current amount of product in inventory, in stock units |

#### ProductCreate

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | yes | The product name |
| `unit` | string | yes | The product's unit of sale (e.g. "each", "bag", "lb") |
| `cost_per_unit` | string | yes | Amount the garden center pays suppliers, in dollars per unit |
| `price_per_unit` | string | yes | Amount the garden center charges customers, in dollars per unit |
| `quantity_in_stock` | string | yes | Current amount of product in inventory, in stock units |

## Postgres Dependencies Installation:

Ensure Postgres is installed, then:

```
pip install sqlalchemy psycopg2-binary
pip freeze > requirements.txt
```

### Database Connection Configuration:

The database connection is configured via `DATABASE_URL`, read at startup, and passed to `create_engine()`:

```
DATABASE_URL = "postgresql://root:root@127.0.0.1:5432/gardendb"
engine = create_engine(DATABASE_URL, echo=True, future=True)
```

### Schema Drop-and-Recreate Behavior

On every app startup during development, the schema is dropped and recreated:

```
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
```
