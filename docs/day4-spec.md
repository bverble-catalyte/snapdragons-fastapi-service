# Day 4 Spec

**B4.1 Persist New Products** 
As a garden center manager, I want new products to be permanently saved when they’re added to the system, so that the catalog doesn’t disappear every time the server restarts.

**F4.1.1** The system shall save created products to a PostgreSQL database.

**F4.1.2** The system shall provide a `POST /products` endpoint for users to create new products.

**F4.1.3** Upon receiving a valid `ProductCreate` request body, the system shall add the product to the database and return a `Product` response body with the product attributes and a status code of `201 Created`.

**F4.1.4** Upon receiving an invalid request body, the system shall return a `422 Unprocessable Entity` response code along with a detailed error message.

**B4.2 View the Full Catalog** 
As a garden center employee, I want to see a list of every product currently in the system, so that I can review what’s in stock.

**F4.2.1** The system shall make all products in the database available to an API user.

**F4.2.2** The system shall provide a `GET /products` endpoint to return a JSON array of `Product` bodies.

**B4.3 Look Up a Single Product** 
As a garden center employee, I want to look up one specific product by its identifier, so that I can quickly check details (price, cost, stock) without scanning the entire catalog.

**F4.3.1** The system shall provide a get product endpoint to locate a product by its unique identifier and view its details. It shall return a `Product` body.

**F4.3.2** The system shall make the get product endpoint available at `GET /products/{id}`.

**F4.3.3** The system shall return a `200 OK` response code if a valid product ID was provided.

**B4.4 Look Up a Product That Doesn't Exist** 
As a garden center employee, I want a clear response when I look up a product that isn’t in the system, so that I know immediately it wasn’t found rather than getting a confusing error or an empty crash.

**F4.4.1** The get product endpoint shall return a `404 Not Found` if the product does not exist.

**B4.5 API Responses Don't Leak Implementation Details** 
As the garden center’s technology partner, I want the data returned by the API to be intentional and controlled – not just whatever happens to be on the internal database object – so that the API has a stable, predictable contract regardless of how the database is structured internally.

**F4.5.1** On a successful `GET /products/{id}` the system shall return a `Product` response body and a `200 OK` response code.

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


# Day 5 Spec

**B5.1 Update an Existing Product**
As a garden center manager, I want to update a product's details (price, cost, stock, name) after it's been created, so that the catalog reflects reality without needing to delete and recreate the item.

**F5.1.1** The system shall update a product and its details.

**F5.1.2** The system shall provide a `PUT /products/{id}` endpoint for users to update existing products.

**F5.1.3** Upon receiving a valid request body for an existing product in the database, the system shall update the product and return a response with a status code of `200 OK` and a `Product` response body.

**F5.1.4** The put product endpoint shall return a `404 Not Found` if the product does not exist.

**F5.1.5** The put product endpoint shall return a `422 Unprocessable Entity` response along with a detailed error message.

**B5.2 Remove a Discontinued Product**
As a garden center manager, I want to permanently remove a product from the catalog, so that discontinued items no longer show up for staff or customers.

**F5.2.1** The system shall provide a `DELETE /products/{id}` endpoint, which removes the product from view for staff and customers, but leaves the underlying data in the database.

**B5.3 Clear Failure When Updating or Deleting Something That Doesn't Exist**
As a garden center employee, I want a clear, correct response when I try to update or delete a product that isn't in the system, so that I know immediately it wasn't found rather than getting a server error or a false success.

**F5.3.1** When the system receives a `DELETE /products/{id}` request for a product that does not exist, the system shall return a `404 Not Found` error.

**B5.4 Reject Invalid Data Before It Reaches the Database**
As the garden center's technology partner, I want obviously invalid input (like a negative price) rejected immediately with a readable explanation, so that bad data never gets a chance to corrupt the catalog and staff aren't left guessing what went wrong.

**F5.4.1** The system shall return a response with a `422 Unprocessable Content` status if any input field is malformed or invalid.

**B5.5 A Predictable, Documented Contract for Every Outcome**
As the garden center's technology partner, I want every endpoint's possible responses, success and failure, documented and verifiable, so that anyone integrating with this API knows exactly what to expect in every case.

**F5.5.1** The system shall provide a `/docs` endpoint that provides a list of all API endpoints, the request/response JSON schemas for the endpoints, and a list of possible response codes for each endpoint.
