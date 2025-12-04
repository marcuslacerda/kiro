import os
from typing import Optional
from fastapi import FastAPI, HTTPException, Query
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field, field_validator
from mangum import Mangum
import boto3
from boto3.dynamodb.conditions import Attr
from botocore.exceptions import ClientError

app = FastAPI(title="Event Management API")

# CORS configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# DynamoDB setup
dynamodb = boto3.resource('dynamodb')
table_name = os.environ.get('EVENTS_TABLE_NAME', 'EventsTable')
table = dynamodb.Table(table_name)


# Pydantic models
class EventBase(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    date: str = Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')
    location: str = Field(..., min_length=1, max_length=200)
    capacity: int = Field(..., gt=0)
    organizer: str = Field(..., min_length=1, max_length=200)
    status: str = Field(..., pattern=r'^(active|cancelled|completed)$')


class EventCreate(EventBase):
    eventId: str = Field(..., min_length=1, max_length=100)


class EventUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    date: Optional[str] = Field(None, pattern=r'^\d{4}-\d{2}-\d{2}$')
    location: Optional[str] = Field(None, min_length=1, max_length=200)
    capacity: Optional[int] = Field(None, gt=0)
    organizer: Optional[str] = Field(None, min_length=1, max_length=200)
    status: Optional[str] = Field(None, pattern=r'^(active|cancelled|completed)$')


class EventResponse(EventBase):
    eventId: str


@app.get("/")
async def root():
    return {"message": "Event Management API", "version": "1.0"}


@app.get("/events", response_model=list[EventResponse])
async def list_events(status: Optional[str] = Query(None, pattern=r'^(active|cancelled|completed)$')):
    """List all events, optionally filtered by status"""
    try:
        if status:
            # Use Attr for filtering - it handles reserved keywords automatically
            response = table.scan(
                FilterExpression=Attr('status').eq(status)
            )
        else:
            response = table.scan()
        
        return response.get('Items', [])
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.post("/events", response_model=EventResponse, status_code=201)
async def create_event(event: EventCreate):
    """Create a new event"""
    try:
        # Check if event already exists
        response = table.get_item(Key={'eventId': event.eventId})
        if 'Item' in response:
            raise HTTPException(status_code=409, detail="Event with this ID already exists")
        
        # Use expression attribute names for reserved keywords
        item = event.model_dump()
        table.put_item(Item=item)
        
        return item
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.get("/events/{event_id}", response_model=EventResponse)
async def get_event(event_id: str):
    """Get a specific event by ID"""
    try:
        response = table.get_item(Key={'eventId': event_id})
        
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Event not found")
        
        return response['Item']
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.put("/events/{event_id}", response_model=EventResponse)
async def update_event(event_id: str, event_update: EventUpdate):
    """Update an existing event"""
    try:
        # Check if event exists
        response = table.get_item(Key={'eventId': event_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Event not found")
        
        # Build update expression dynamically
        update_data = event_update.model_dump(exclude_unset=True)
        if not update_data:
            raise HTTPException(status_code=400, detail="No fields to update")
        
        # Use expression attribute names for reserved keywords
        expression_attribute_names = {}
        expression_attribute_values = {}
        update_expressions = []
        
        reserved_keywords = {'status', 'capacity', 'location', 'date'}
        
        for key, value in update_data.items():
            if key in reserved_keywords:
                attr_name = f'#{key}'
                expression_attribute_names[attr_name] = key
                expression_attribute_values[f':{key}'] = value
                update_expressions.append(f'{attr_name} = :{key}')
            else:
                expression_attribute_values[f':{key}'] = value
                update_expressions.append(f'{key} = :{key}')
        
        update_expression = 'SET ' + ', '.join(update_expressions)
        
        # Perform update
        update_params = {
            'Key': {'eventId': event_id},
            'UpdateExpression': update_expression,
            'ExpressionAttributeValues': expression_attribute_values,
            'ReturnValues': 'ALL_NEW'
        }
        
        if expression_attribute_names:
            update_params['ExpressionAttributeNames'] = expression_attribute_names
        
        response = table.update_item(**update_params)
        
        return response['Attributes']
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


@app.delete("/events/{event_id}", status_code=200)
async def delete_event(event_id: str):
    """Delete an event"""
    try:
        # Check if event exists
        response = table.get_item(Key={'eventId': event_id})
        if 'Item' not in response:
            raise HTTPException(status_code=404, detail="Event not found")
        
        table.delete_item(Key={'eventId': event_id})
        
        return {"message": "Event deleted successfully", "eventId": event_id}
    except ClientError as e:
        raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")


# Lambda handler
handler = Mangum(app)
