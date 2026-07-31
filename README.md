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

| Method | Path | Requires Auth | Description |
| --- | --- | --- | --- |
| `GET` | `/db-check` | No | [Database Check](#get-db-check)
| `GET` | `/products` | No | [View Products](#get-products)
| `POST` | `/products` | **Yes** | [Create Product](#post-products)
| `GET` | `/products/{id}` | No | [View Product](#get-productsid)
| `PUT` | `/products/{id}` | **Yes** | [Update Product](#put-productsid)
| `DELETE` | `/products/{id}` | **Yes** | [Delete Product](#delete-productsid)
| `GET` | `/categories` | No | [View Categories](#get-categories)
| `POST` | `/categories` | **Yes** | [Create Category](#post-categories)
| `GET` | `/categories/{id}` | No | [View Category](#get-categoriesid)
| `GET` | `/categories/{id}/products` | No | [View Products for Category](#get-categoriesidproducts)
| `PUT` | `/categories/{id}` | **Yes** | [Update Category](#put-categoriesid)
| `DELETE` | `/categories/{id}` | **Yes** | [Delete Category](#delete-categoriesid)
| `POST` | `/tokens` | No | [Create Token](#post-tokens)

### Authorization

Some endpoints require authorization via JWT. See the [create token](#post-tokens) endpoint for details.

### `GET` /db-check

**Database Check**

Check the status of the database connection.

**Responses**

| Status | Description | Body |
| --- | --- | --- |
| `200` | The connection status | `application/json` [`DatabaseStatus`](#databasestatus) |

[Back to Summary](#summary)

---

### `GET` /products

**View Products**

View all products in the database, optionally filtered by name and/or unit of sale.

The name search will be performed on a normalized product name (lowercased and with whitespace stripped). In other words, `"3in"` will match against a product named `"3 In. Planter"`.

**Parameters**

| Name | In | Type | Required | Notes |
| --- | --- | --- | --- | --- |
| `name` | query | string | no | |
| `unit` | query | string | no | |

**Responses**

| Status | Description | Body |
| --- | --- | --- |
| `200` | The list of products | `application/json` array[[`ProductRead`](#productread)] |

[Back to Summary](#summary)

---

### `POST` /products

**Create Product**

Create a new product.

**Request body** (required)

`application/json` — [`ProductCreate`](#productcreate)

**Request Headers**

| Name | Required | Contents | Notes |
| --- | --- | --- | --- |
| Authorization | Yes | `"Bearer: ACCESS_TOKEN"` | See [Authorization](#authorization)

**Responses**

| Status | Description | Body |
| --- | --- | --- |
| `201` | The newly created product | `application/json` [`ProductRead`](#productread) |
| `401` | The client is not authenticated | — |
| `404` | The category referenced by `category_id` does not exist. | — |
| `422` | Validation Error | `application/json` [`HTTPValidationError`](#httpvalidationerror) |

[Back to Summary](#summary)

---

### `GET` /products/{id}

**View Product**

View a product with a given ID.

**Parameters**

| Name | In | Type | Required | Notes |
| --- | --- | --- | --- | --- |
| `id` | path | int | yes |  |

**Responses**

| Status | Description | Body |
| --- | --- | --- |
| `200` | The product | `application/json` [`ProductRead`](#productread) |
| `404` | A product with that ID does not exist. | — |
| `422` | Validation Error | `application/json` [`HTTPValidationError`](#httpvalidationerror) |

[Back to Summary](#summary)

---

### `PUT` /products/{id}

**Update Product**

Update a product with a given ID.

**Parameters**

| Name | In | Type | Required | Notes |
| --- | --- | --- | --- | --- |
| `id` | path | int | yes |  |

**Request body** (required)

`application/json` — [`ProductCreate`](#productcreate)

**Request Headers**

| Name | Required | Contents | Notes |
| --- | --- | --- | --- |
| Authorization | Yes | `"Bearer: ACCESS_TOKEN"` | See [Authorization](#authorization)

**Responses**

| Status | Description | Body |
| --- | --- | --- |
| `200` | The updated product | `application/json` [`ProductRead`](#productread) |
| `401` | The client is not authenticated | — |
| `404` | A product with that ID does not exist, or the category referenced by `category_id` does not exist. | — |
| `422` | Validation Error | `application/json` [`HTTPValidationError`](#httpvalidationerror) |

[Back to Summary](#summary)

---

### `DELETE` /products/{id}

**Delete Product**

Delete a product with a given ID.

**Parameters**

| Name | In | Type | Required | Notes |
| --- | --- | --- | --- | --- |
| `id` | path | int | yes |  |

**Request Headers**

| Name | Required | Contents | Notes |
| --- | --- | --- | --- |
| Authorization | Yes | `"Bearer: ACCESS_TOKEN"` | See [Authorization](#authorization)

**Responses**

| Status | Description | Body |
| --- | --- | --- |
| `204` | The product was deleted successfully. | — |
| `401` | The client is not authenticated | — |
| `404` | A product with that ID does not exist. | — |
| `422` | Validation Error | `application/json` [`HTTPValidationError`](#httpvalidationerror) |

[Back to Summary](#summary)

---

### `GET` /categories

**View Categories**

View all categories in the database.

The name search will be performed on a normalized category name (lowercased and with whitespace stripped). In other words, `"pot"` will match against a category named `"Pots and Planters"`.

**Parameters**

| Name | In | Type | Required | Notes |
| --- | --- | --- | --- | --- |
| `name` | query | string | no | |

**Responses**

| Status | Description | Body |
| --- | --- | --- |
| `200` | The list of categories | `application/json` array[[`CategoryRead`](#categoryread)] |

[Back to Summary](#summary)

---

### `POST` /categories

**Create Category**

Create a new category.

**Request body** (required)

`application/json` — [`CategoryCreate`](#categorycreate)

**Request Headers**

| Name | Required | Contents | Notes |
| --- | --- | --- | --- |
| Authorization | Yes | `"Bearer: ACCESS_TOKEN"` | See [Authorization](#authorization)

**Responses**

| Status | Description | Body |
| --- | --- | --- |
| `201` | The newly created category | `application/json` [`CategoryRead`](#categoryread) |
| `401` | The client is not authenticated | — |
| `422` | Validation Error | `application/json` [`HTTPValidationError`](#httpvalidationerror) |

[Back to Summary](#summary)

---

### `GET` /categories/{id}

**View Category**

View a category with a given ID.

**Parameters**

| Name | In | Type | Required | Notes |
| --- | --- | --- | --- | --- |
| `id` | path | int | yes |  |

**Responses**

| Status | Description | Body |
| --- | --- | --- |
| `200` | The category | `application/json` [`CategoryRead`](#categoryread) |
| `404` | A category with that ID does not exist. | — |
| `422` | Validation Error | `application/json` [`HTTPValidationError`](#httpvalidationerror) |

[Back to Summary](#summary)

---

### `GET` /categories/{id}/products

**View Products for Category**

View a category with a given ID and all its associated products.

**Parameters**

| Name | In | Type | Required | Notes |
| --- | --- | --- | --- | --- |
| `id` | path | int | yes |  |

**Responses**

| Status | Description | Body |
| --- | --- | --- |
| `200` | The category, with its associated products | `application/json` [`CategoryReadWithProducts`](#categoryreadwithproducts) |
| `404` | A category with that ID does not exist. | — |
| `422` | Validation Error | `application/json` [`HTTPValidationError`](#httpvalidationerror) |

[Back to Summary](#summary)

---

### `PUT` /categories/{id}

**Update Category**

Update a category with a given ID.

**Parameters**

| Name | In | Type | Required | Notes |
| --- | --- | --- | --- | --- |
| `id` | path | int | yes |  |

**Request body** (required)

`application/json` — [`CategoryCreate`](#categorycreate)

**Request Headers**

| Name | Required | Contents | Notes |
| --- | --- | --- | --- |
| Authorization | Yes | `"Bearer: ACCESS_TOKEN"` | See [Authorization](#authorization)

**Responses**

| Status | Description | Body |
| --- | --- | --- |
| `200` | The updated category | `application/json` [`CategoryRead`](#categoryread) |
| `401` | The client is not authenticated | — |
| `404` | A category with that ID does not exist. | — |
| `422` | Validation Error | `application/json` [`HTTPValidationError`](#httpvalidationerror) |

[Back to Summary](#summary)

---

### `DELETE` /categories/{id}

**Delete Category**

Soft deletes category based on given ID.

**Parameters**

| Name | In | Type | Required | Notes |
| --- | --- | --- | --- | --- |
| `id` | path | int | yes |  |

**Request Headers**

| Name | Required | Contents | Notes |
| --- | --- | --- | --- |
| Authorization | Yes | `"Bearer: ACCESS_TOKEN"` | See [Authorization](#authorization)

**Responses**

| Status | Description | Body |
| --- | --- | --- |
| `204` | The category was deleted successfully. | — |
| `401` | The client is not authenticated | — |
| `404` | A category with that ID does not exist. | — |
| `409` | The category must not have any products associated with it. | — |
| `422` | Validation Error | `application/json` [`HTTPValidationError`](#httpvalidationerror) |

[Back to Summary](#summary)

---

### `POST` /tokens

**Create Token (Login)**

Create a new session token in order to access protected endpoints.

**Request body** (required)

`application/json` — [`UserCredentials`](#usercredentials)

**Responses**

| Status | Description | Body |
| --- | --- | --- |
| `201` | The token was created successfully. | [`TokenRead`](#tokenread) |
| `401` | Invalid username or password provided. | — |
| `422` | Validation Error | `application/json` [`HTTPValidationError`](#httpvalidationerror) |

[Back to Summary](#summary)

---

## Schemas

### CategoryCreate

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `name` | string | yes | The name of the category, min length `1` |

### CategoryRead

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `id` | int | yes | The unique category identifier, min (exclusive) `0` |
| `name` | string | yes | The name of the category, min length `1` |

### CategoryReadWithProducts

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `id` | int | yes | The unique category identifier, min (exclusive) `0` |
| `name` | string | yes | The name of the category, min length `1` |
| `products` | array[[`ProductReadWithoutCategory`](#productreadwithoutcategory)] | yes | min length `0` |

### DatabaseStatus

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `status` | string | yes | Database connection status |
| `product_count` | int | yes | The number of rows in the product table |

### HTTPValidationError

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `detail` | array[[`ValidationError`](#validationerror)] | no |  |


### ProductCreate

Input schema for creating a new product. Does not include `id`, since this will be assigned on creation.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `name` | string | yes | The product name, min length `1` |
| `unit` | string | yes | The product's unit of sale (e.g. "each", "bag", "lb"), min length `1` |
| `cost_per_unit` | string | yes | Amount the garden center pays suppliers, in dollars per unit, min (exclusive) `0.0` |
| `price_per_unit` | string | yes | Amount the garden center charges customers, in dollars per unit, min (exclusive) `0.0` |
| `quantity_in_stock` | string | yes | Current amount of product in inventory, in stock units, min `0.0` |
| `category_id` | int | yes | The ID of the category this product belongs to, min (exclusive) `0` |

### ProductRead

Represents a product sold by the garden center.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `id` | int | yes | The unique product identifier, min (exclusive) `0` |
| `name` | string | yes | The product name, min length `1` |
| `unit` | string | yes | The product's unit of sale (e.g. "each", "bag", "lb"), min length `1` |
| `cost_per_unit` | string | yes | Amount the garden center pays suppliers, in dollars per unit, min (exclusive) `0.0` |
| `price_per_unit` | string | yes | Amount the garden center charges customers, in dollars per unit, min (exclusive) `0.0` |
| `quantity_in_stock` | string | yes | Current amount of product in inventory, in stock units, min `0.0` |
| `category` | [`CategoryRead`](#categoryread) | yes | The category this product belongs to |

### ProductReadWithoutCategory

Represents a product without its parent category. Used where the product is already nested under its category (see [`CategoryReadWithProducts`](#categoryreadwithproducts)), so repeating the category would just duplicate data the caller already has.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `id` | int | yes | The unique product identifier, min (exclusive) `0` |
| `name` | string | yes | The product name, min length `1` |
| `unit` | string | yes | The product's unit of sale (e.g. "each", "bag", "lb"), min length `1` |
| `cost_per_unit` | string | yes | Amount the garden center pays suppliers, in dollars per unit, min (exclusive) `0.0` |
| `price_per_unit` | string | yes | Amount the garden center charges customers, in dollars per unit, min (exclusive) `0.0` |
| `quantity_in_stock` | string | yes | Current amount of product in inventory, in stock units, min `0.0` |

### TokenRead

Contains information about a newly generated access token.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `access_token` | string | yes | A JWT for API access |
| `token_type` | string | yes | Always `"bearer"` |

### UserCredentials

An object containing login information.

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `username` | string | yes |  |
| `password` | string | yes |  |

### ValidationError

| Field | Type | Required | Notes |
| --- | --- | --- | --- |
| `loc` | array[string \| int] | yes |  |
| `msg` | string | yes |  |
| `type` | string | yes |  |
| `input` | any | no |  |
| `ctx` | object | no |  |

## Postgres Dependencies Installation:

Ensure Postgres is installed, then:

```
pip install sqlalchemy psycopg2-binary python-dotenv
pip freeze > requirements.txt
```

## Database Connection Configuration:

The database credentials are read from environment variables via `src/config.py`, which loads them from a `.env` file at the project root using `python-dotenv`.

1. Copy the example file and fill in your local values:
```bash
cp .env-example .env
```

2. '.env' should define:
```dotenv
DB_USER=your_db_user
DB_PASSWORD=your_db_password
DB_HOST=localhost
DB_PORT=5432
DB_NAME=your_db_name
TEST_DB_NAME=your_test_db_name
```

3. `config.py` validates the environment variables on import, raises `RunTimeError` if an area is missing, and exposes a `Settings` instances for building connection URLs:
```python
from config import settings

engine = create_engine(settings.database_url(), echo=True, future=True)
```

### Building Connection URLs
Both `.database_url()` and `.test_database_url()` of `settings` builds a Postgres URL using the same credentials, and defaults to `DB_NAME` and `TEST_DB_NAME` respectively. Otherwise, they accept an explicit database name pointing to a different database in the server.

### Schema Drop-and-Recreate Behavior

On every app startup during development, the schema is dropped and recreated:

```
Base.metadata.drop_all(bind=engine)
Base.metadata.create_all(bind=engine)
```
