# Day 4 Spec

**B1** As a garden center manager, I want new products to be permanently saved when they’re added to the system, so that the catalog doesn’t disappear every time the server restarts.

**F1.1** The system shall save created products to a PostgreSQL database.

**F1.2** The system shall provide a `POST /products` endpoint for users to create new products.

**F1.3** Upon receiving a valid `ProductCreate` request body, the system shall add the product to the database and return a `Product` response body with the product attributes and a status code of `201 Created`.

**F1.4** Upon receiving an invalid request body, the system shall return a `422 Unprocessable Entity` response code along with a detailed error message.

**B2.** As a garden center employee, I want to see a list of every product currently in the system, so that I can review what’s in stock.

**F2.1** The system shall make all products in the database available to an API user.

**F2.2** The system shall provide a `GET /products` endpoint to return a JSON array of `Product` bodies.

**B3.** As a garden center employee, I want to look up one specific product by its identifier, so that I can quickly check details (price, cost, stock) without scanning the entire catalog.

**F3.1** The system shall provide a get product endpoint to locate a product by its unique identifier and view its details. It shall return a `Product` body.

**F3.2** The system shall make the get product endpoint available at `GET /products/{id}`.

**F3.3** The system shall return a `200 OK` response code if a valid product ID was provided.

**B4.** As a garden center employee, I want a clear response when I look up a product that isn’t in the system, so that I know immediately it wasn’t found rather than getting a confusing error or an empty crash.

**F4.1** The get product endpoint shall return a `404 Not Found` if the product does not exist.

**B5** As the garden center’s technology partner, I want the data returned by the API to be intentional and controlled – not just whatever happens to be on the internal database object – so that the API has a stable, predictable contract regardless of how the database is structured internally.

**F5.1** On a successful `GET /products/{id}` the system shall return a `Product` response body and a `200 OK` response code.

## JSON Schemas

### Product

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `id` | int | yes | The product's unique identifier |
| `name` | string | yes | The product name |
| `unit` | string | yes | The product's unit of sale (e.g. "each", "bag", "lb") |
| `cost_per_unit` | string | yes | Amount the garden center pays suppliers, in dollars per unit |
| `price_per_unit` | string | yes | Amount the garden center charges customers, in dollars per unit |
| `quantity_in_stock` | string | yes | Current amount of product in inventory, in stock units |

### ProductCreate

| Field | Type | Required | Description |
| --- | --- | --- | --- |
| `name` | string | yes | The product name |
| `unit` | string | yes | The product's unit of sale (e.g. "each", "bag", "lb") |
| `cost_per_unit` | string | yes | Amount the garden center pays suppliers, in dollars per unit |
| `price_per_unit` | string | yes | Amount the garden center charges customers, in dollars per unit |
| `quantity_in_stock` | string | yes | Current amount of product in inventory, in stock units |
