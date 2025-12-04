# Event Management API

A serverless event management application built with FastAPI, AWS Lambda, API Gateway, and DynamoDB.

## Architecture

- **Backend**: FastAPI REST API with Pydantic validation
- **Database**: DynamoDB (serverless NoSQL)
- **Compute**: AWS Lambda (Python 3.12)
- **API Gateway**: REST API with CORS enabled
- **Infrastructure**: AWS CDK (TypeScript)

## Features

- ✅ Full CRUD operations for events
- ✅ Input validation with Pydantic
- ✅ Proper handling of DynamoDB reserved keywords
- ✅ CORS configuration for web access
- ✅ Error handling and HTTP status codes
- ✅ Serverless deployment with AWS Lambda

## Event Schema

```json
{
  "eventId": "string (required, unique)",
  "title": "string (1-200 chars)",
  "description": "string (1-1000 chars)",
  "date": "string (YYYY-MM-DD format)",
  "location": "string (1-200 chars)",
  "capacity": "integer (> 0)",
  "organizer": "string (1-200 chars)",
  "status": "string (active|cancelled|completed)"
}
```

## API Documentation

📚 **[View Full API Documentation](backend/docs/index.html)** - Complete interactive API reference

### Base URL
```
https://iqsojot0q9.execute-api.us-west-2.amazonaws.com/prod/
```

### Endpoints

#### 1. List All Events
```bash
GET /events
GET /events?status=active
```

#### 2. Create Event
```bash
POST /events
Content-Type: application/json

{
  "eventId": "event-123",
  "title": "Tech Conference 2024",
  "description": "Annual technology conference",
  "date": "2024-12-15",
  "location": "San Francisco",
  "capacity": 500,
  "organizer": "Tech Corp",
  "status": "active"
}
```

#### 3. Get Event by ID
```bash
GET /events/{eventId}
```

#### 4. Update Event
```bash
PUT /events/{eventId}
Content-Type: application/json

{
  "title": "Updated Title",
  "capacity": 600
}
```

#### 5. Delete Event
```bash
DELETE /events/{eventId}
```

## Deployment

### Prerequisites

- Node.js 18+ and npm
- Python 3.12+
- AWS CLI configured with credentials
- AWS CDK CLI: `npm install -g aws-cdk`

### Steps

1. **Install backend dependencies**:
```bash
cd backend
pip3 install -r requirements.txt -t lambda_package/ --platform manylinux2014_x86_64 --only-binary=:all: --python-version 3.12
cp main.py lambda_package/
```

2. **Install infrastructure dependencies**:
```bash
cd infrastructure
npm install
```

3. **Bootstrap CDK** (first time only):
```bash
npx cdk bootstrap
```

4. **Deploy**:
```bash
npm run build
npx cdk deploy
```

5. **Get API endpoint**:
The deployment will output the API Gateway URL.

## Testing

Run the test suite:

```bash
# List events
curl -X GET "https://YOUR-API-URL/prod/events"

# Create event
curl -X POST "https://YOUR-API-URL/prod/events" \
  -H "Content-Type: application/json" \
  -d '{
    "eventId": "test-event-1",
    "title": "Test Event",
    "description": "Testing the API",
    "date": "2024-12-15",
    "location": "Test Location",
    "capacity": 100,
    "organizer": "Test Organizer",
    "status": "active"
  }'

# Get event
curl -X GET "https://YOUR-API-URL/prod/events/test-event-1"

# Update event
curl -X PUT "https://YOUR-API-URL/prod/events/test-event-1" \
  -H "Content-Type: application/json" \
  -d '{"capacity": 150}'

# Delete event
curl -X DELETE "https://YOUR-API-URL/prod/events/test-event-1"
```

## Development

### Local Testing (Backend)

```bash
cd backend
pip install -r requirements.txt
uvicorn main:app --reload
```

Visit `http://localhost:8000/docs` for interactive API documentation.

### Update and Redeploy

After making changes to the backend:

```bash
cd backend
cp main.py lambda_package/
cd ../infrastructure
npx cdk deploy
```

## Clean Up

To remove all AWS resources:

```bash
cd infrastructure
npx cdk destroy
```

## Technical Notes

- **DynamoDB Reserved Keywords**: The API properly handles reserved keywords like `status`, `capacity`, `location`, and `date` using boto3's `Attr` for filtering and expression attribute names for updates.
- **CORS**: Configured to allow all origins for development. Restrict in production.
- **Validation**: Pydantic v2 with `pattern` parameter for regex validation.
- **Lambda Handler**: Uses Mangum to adapt FastAPI for AWS Lambda.
- **Deployment Package**: Pre-built dependencies to avoid Docker requirement during CDK deployment.

## Project Structure

```
.
├── backend/
│   ├── main.py              # FastAPI application
│   ├── requirements.txt     # Python dependencies
│   └── lambda_package/      # Deployment package
├── infrastructure/
│   ├── lib/
│   │   └── infrastructure-stack.ts  # CDK stack definition
│   ├── bin/
│   ├── package.json
│   └── tsconfig.json
└── README.md
```

## Test Results

All endpoints tested successfully:

✅ GET /events - Status: 200  
✅ GET /events?status=active - Status: 200  
✅ POST /events - Status: 201  
✅ GET /events/{eventId} - Status: 200  
✅ PUT /events/{eventId} - Status: 200  
✅ DELETE /events/{eventId} - Status: 200
