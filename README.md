# Sea is a simple, lightweight, and fast web server for storing and serving json data.

## Explanation of Fish and Sea

### Sea

A sea is like a bucket that contains fishes. It has a name and a description as well as a unique identifier. The sea can contain multiple fishes.
The unique identifier can be used to retrieve the sea and all the fishes it contains.

### Fish

A fish is a json object that contains a name, description, and data. The data can be any json object that describes the fish. The fish also has a unique identifier that can be used to retrieve the fish from the sea.

## What is the point of all this?

The point was to create a simple web server that can store and serve json data for free. The server is lightweight and fast, and it can be used to store and serve any json data you want. The lack of authentication and authorization makes it easy to use, but it also makes it insecure. This server is not meant to be used in production, but it can be used for testing and development purposes. It can also be used by anyone who wants to store and serve json data for free with minimal effort.

# Usage

## Sea

### Create a Sea

To create a new sea, send a POST request to `/V1/sea/` with the following JSON body:

```json
{
  "name": "Pacific Ocean",
  "description": "The largest ocean on Earth."
}
```

Response:

- `201 Created`: Returns the created sea object.
- `404 Not Found`: The resource was not found.
- `500 Internal Server Error`: The server encountered an unexpected condition.
- `422 Unprocessable Entity`: Validation error.

### Get a Sea

To retrieve a sea, send a GET request to `/V1/sea/{sea_id}`:

```http
GET /V1/sea/Sea-1234567890abcdef
```

Response:

- `200 OK`: Returns the sea object.
- `404 Not Found`: The resource was not found.
- `500 Internal Server Error`: The server encountered an unexpected condition.
- `422 Unprocessable Entity`: Validation error.

### Delete a Sea

To delete a sea, send a DELETE request to `/V1/sea/{sea_id}`:

```http
DELETE /V1/sea/Sea-1234567890abcdef
```

Response:

- `200 OK`: Successful response.
- `404 Not Found`: The resource was not found.
- `500 Internal Server Error`: The server encountered an unexpected condition.
- `422 Unprocessable Entity`: Validation error.

---

## Fish

### Create a Fish

To create a new fish, send a POST request to `/V1/sea/{sea_id}/fish/` with the following JSON body:

```json
{
  "name": "Nemo",
  "description": "A small orange fish.",
  "data": {
    "color": "orange",
    "size": "small"
  }
}
```

Response:

- `201 Created`: Returns the created fish object.
- `404 Not Found`: The resource was not found.
- `500 Internal Server Error`: The server encountered an unexpected condition.
- `422 Unprocessable Entity`: Validation error.

### Get Fishes

To retrieve all fishes in a sea, send a GET request to `/V1/sea/{sea_id}/fish/`:

```http
GET /V1/sea/Sea-1234567890abcdef/fish/
```

Response:

- `200 OK`: Returns an array of fish objects.
- `404 Not Found`: The resource was not found.
- `500 Internal Server Error`: The server encountered an unexpected condition.
- `422 Unprocessable Entity`: Validation error.

### Get a Fish

To retrieve a specific fish, send a GET request to `/V1/sea/{sea_id}/fish/{fish_id}`:

```http
GET /V1/sea/Sea-1234567890abcdef/fish/Fish-1234567890abcdef
```

Response:

- `200 OK`: Returns the fish object.
- `404 Not Found`: The resource was not found.
- `500 Internal Server Error`: The server encountered an unexpected condition.
- `422 Unprocessable Entity`: Validation error.

### Delete a Fish

To delete a specific fish, send a DELETE request to `/V1/sea/{sea_id}/fish/{fish_id}`:

```http
DELETE /V1/sea/Sea-1234567890abcdef/fish/Fish-1234567890abcdef
```

Response:

- `200 OK`: Successful response.
- `404 Not Found`: The resource was not found.
- `500 Internal Server Error`: The server encountered an unexpected condition.
- `422 Unprocessable Entity`: Validation error.

### Get Stats

To retrieve statistics, send a GET request to `/stats`:

```http
GET /stats
```

Response:

- `200 OK`: Returns the statistics object.
- `404 Not Found`: The resource was not found.
- `500 Internal Server Error`: The server encountered an unexpected condition.

### Read Root

To read the root endpoint, send a GET request to `/`:

```http
GET /
```

Response:

- `200 OK`: Successful response.
