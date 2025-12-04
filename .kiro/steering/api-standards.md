---
inclusion: fileMatch
fileMatchPattern: '**/*{api,route,endpoint,handler,main}*.{py,ts,js}'
---

# REST API Standards and Conventions

This document defines the REST API standards for this project. Apply these conventions when creating or modifying API endpoints.

## HTTP Methods

Use HTTP methods according to their semantic meaning:

- **GET**: Retrieve resources (read-only, idempotent, cacheable)
- **POST**: Create new resources (non-idempotent)
- **PUT**: Update entire resources (idempotent)
- **PATCH**: Partial update of resources (idempotent)
- **DELETE**: Remove resources (idempotent)

## HTTP Status Codes

Use appropriate status codes for different scenarios:

### Success Codes (2xx)
- **200 OK**: Successful GET, PUT, PATCH, or DELETE
- **201 Created**: Successful POST that creates a resource
- **204 No Content**: Successful request with no response body (alternative for DELETE)

### Client Error Codes (4xx)
- **400 Bad Request**: Invalid request format or missing required fields
- **404 Not Found**: Resource doesn't exist
- **409 Conflict**: Resource already exists or conflict with current state
- **422 Unprocessable Entity**: Validation errors

### Server Error Codes (5xx)
- **500 Internal Server Error**: Unexpected server errors

## URL Structure

- Use **plural nouns** for resource collections: `/events`, `/users`
- Use **path parameters** for resource IDs: `/events/{eventId}`
- Use **query parameters** for filtering, sorting, pagination: `/events?status=active&limit=10`
- Keep URLs **lowercase** and use **hyphens** for multi-word resources: `/event-registrations`

## JSON Response Format

### Success Response
```json
{
  "id": "resource-id",
  "field1": "value1",
  "field2": "value2"
}
```

For collections:
```json
[
  {"id": "1", "name": "Item 1"},
  {"id": "2", "name": "Item 2"}
]
```

### Error Response
```json
{
  "detail": "Human-readable error message"
}
```

For validation errors (422):
```json
{
  "detail": [
    {
      "loc": ["body", "fieldName"],
      "msg": "Field validation error message",
      "type": "validation_error"
    }
  ]
}
```

## Request/Response Headers

### Content Type
- Always use `Content-Type: application/json` for JSON payloads
- Set appropriate `Content-Type` in responses

### CORS Headers
- Include CORS headers for web client access
- For development: Allow all origins
- For production: Restrict to specific domains

## Naming Conventions

### Field Names
- Use **camelCase** for JSON field names: `eventId`, `firstName`, `createdAt`
- Be consistent across all endpoints
- Use descriptive names that clearly indicate the field's purpose

### Date/Time Format
- Use **ISO 8601** format for dates: `YYYY-MM-DD`
- Use **ISO 8601** format for timestamps: `YYYY-MM-DDTHH:mm:ss.sssZ`

## Validation

- Validate all input data before processing
- Return **422 Unprocessable Entity** for validation errors
- Provide clear, actionable error messages
- Validate:
  - Required fields are present
  - Data types are correct
  - String lengths are within bounds
  - Numeric values are within valid ranges
  - Enum values are from allowed set
  - Date formats are valid

## Idempotency

- **GET, PUT, PATCH, DELETE** should be idempotent
- Multiple identical requests should have the same effect as a single request
- **POST** is not idempotent (creates new resources each time)

## Error Handling

- Always catch and handle exceptions gracefully
- Never expose internal error details or stack traces to clients
- Log detailed errors server-side for debugging
- Return user-friendly error messages in responses
- Use appropriate HTTP status codes for different error types

## Resource Operations

### List Resources (GET /resources)
- Support filtering via query parameters
- Return array of resources
- Status: 200 OK

### Get Single Resource (GET /resources/{id})
- Return single resource object
- Status: 200 OK
- Status: 404 Not Found if resource doesn't exist

### Create Resource (POST /resources)
- Accept resource data in request body
- Validate all required fields
- Return created resource with generated ID
- Status: 201 Created
- Status: 409 Conflict if resource already exists
- Status: 422 Unprocessable Entity for validation errors

### Update Resource (PUT /resources/{id})
- Accept complete or partial resource data
- Validate updated fields
- Return updated resource
- Status: 200 OK
- Status: 404 Not Found if resource doesn't exist
- Status: 422 Unprocessable Entity for validation errors

### Delete Resource (DELETE /resources/{id})
- Remove the resource
- Return confirmation message or 204 No Content
- Status: 200 OK or 204 No Content
- Status: 404 Not Found if resource doesn't exist

## Best Practices

1. **Be Consistent**: Use the same patterns across all endpoints
2. **Be Predictable**: Follow REST conventions so APIs are intuitive
3. **Be Clear**: Use descriptive names and provide helpful error messages
4. **Be Efficient**: Return only necessary data, support filtering
5. **Be Versioned**: Consider API versioning for future changes (e.g., `/v1/events`)

## FastAPI Specific

When using FastAPI:
- Use Pydantic models for request/response validation
- Leverage FastAPI's automatic OpenAPI documentation
- Use `response_model` parameter to define response schemas
- Use `status_code` parameter to set default status codes
- Use `HTTPException` for error responses
- Use dependency injection for shared logic

## Example Implementation

```python
from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field

app = FastAPI()

class ItemCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)

class ItemResponse(BaseModel):
    id: str
    name: str
    description: str

@app.get("/items", response_model=list[ItemResponse])
async def list_items(status: str = Query(None)):
    # Implementation
    pass

@app.post("/items", response_model=ItemResponse, status_code=201)
async def create_item(item: ItemCreate):
    # Check if exists
    if exists:
        raise HTTPException(status_code=409, detail="Item already exists")
    # Create and return
    pass

@app.get("/items/{item_id}", response_model=ItemResponse)
async def get_item(item_id: str):
    if not found:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@app.put("/items/{item_id}", response_model=ItemResponse)
async def update_item(item_id: str, item: ItemCreate):
    if not found:
        raise HTTPException(status_code=404, detail="Item not found")
    # Update and return
    pass

@app.delete("/items/{item_id}")
async def delete_item(item_id: str):
    if not found:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted successfully"}
```
