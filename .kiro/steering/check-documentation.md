---
inclusion: always
---

# Documentation and Context Checking

## Important Reminder

When creating or updating Python, CDK, or AWS-related code, **always check the documentation/context** first to ensure you're using the latest APIs, best practices, and correct syntax.

## When to Check Documentation

Check documentation/context when:
- Creating or modifying Python code (especially with FastAPI, Pydantic, boto3)
- Writing or updating AWS CDK infrastructure code
- Using AWS services (Lambda, DynamoDB, API Gateway, etc.)
- Implementing new features or libraries
- Encountering deprecated APIs or syntax
- Unsure about the correct way to implement something

## Key Areas to Verify

### Python Libraries
- **Pydantic**: Check for v2 syntax changes (e.g., `pattern` vs `regex`, `model_dump` vs `dict`)
- **FastAPI**: Verify latest decorator syntax, dependency injection patterns
- **boto3**: Confirm correct service client methods and parameters
- **DynamoDB**: Check for reserved keywords and proper expression attribute handling

### AWS CDK
- **Construct versions**: Verify you're using the correct CDK v2 constructs
- **Lambda functions**: Check for latest runtime versions and configuration options
- **API Gateway**: Verify CORS configuration and integration patterns
- **Best practices**: Confirm removal policies, naming conventions, and resource configurations

### AWS Services
- **Regional availability**: Check if services/features are available in target regions
- **API changes**: Verify method signatures and parameters
- **Deprecated features**: Avoid using deprecated APIs or services

## How to Check

Use the available MCP tools to search documentation:

```
# Search AWS documentation
mcp_aws_knowledge_mcp_server_aws___search_documentation
- Topics: reference_documentation, cdk_docs, cdk_constructs, etc.

# Read specific documentation pages
mcp_aws_knowledge_mcp_server_aws___read_documentation

# Check regional availability
mcp_aws_knowledge_mcp_server_aws___get_regional_availability
```

## Common Pitfalls to Avoid

### Pydantic v2 Changes
```python
# Old (v1): regex parameter
Field(..., regex=r'^\d{4}-\d{2}-\d{2}$')

# New (v2): pattern parameter
Field(..., pattern=r'^\d{4}-\d{2}-\d{2}$')

# Old (v1): .dict()
model.dict()

# New (v2): .model_dump()
model.model_dump()
```

### DynamoDB Reserved Keywords
```python
# Always check if attribute names are reserved keywords
# Reserved: status, capacity, location, date, etc.

# Use Attr for filtering
from boto3.dynamodb.conditions import Attr
response = table.scan(FilterExpression=Attr('status').eq('active'))

# Use ExpressionAttributeNames for updates
table.update_item(
    Key={'id': 'item-1'},
    UpdateExpression='SET #st = :status',
    ExpressionAttributeNames={'#st': 'status'},
    ExpressionAttributeValues={':status': 'active'}
)
```

### CDK Best Practices
```typescript
// Check for latest construct patterns
import * as lambda from 'aws-cdk-lib/aws-lambda';
import * as apigateway from 'aws-cdk-lib/aws-apigateway';

// Verify runtime versions are current
runtime: lambda.Runtime.PYTHON_3_12  // Check if newer version available

// Confirm proper resource naming and tagging
```

## Documentation Search Strategy

1. **Start broad**: Search for the general topic or service
2. **Get specific**: Look for exact API methods or patterns
3. **Check examples**: Find code examples and patterns
4. **Verify versions**: Ensure documentation matches your library versions
5. **Read recommendations**: Look for AWS recommendations and best practices

## Example Workflow

When implementing a new feature:

1. Search documentation for the service/library
2. Review API reference for correct method signatures
3. Check for code examples and patterns
4. Verify any deprecated features to avoid
5. Implement using current best practices
6. Test thoroughly

## Remember

- **Don't assume**: APIs change, syntax evolves, best practices update
- **Check first**: A few minutes of documentation review saves hours of debugging
- **Stay current**: Use the latest stable versions and recommended patterns
- **Learn from examples**: Official examples often show best practices

**When in doubt, check the documentation!** It's always better to verify than to use outdated or incorrect patterns.
