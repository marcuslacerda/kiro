---
inclusion: always
---

# Credentials and Sensitive Information Handling

## Important Reminder

When working with code that requires credentials, API keys, tokens, or other sensitive information:

1. **Always prompt the user** before hardcoding any credentials
2. **Never commit credentials** to version control
3. **Use environment variables** for sensitive data
4. **Check for existing credentials** in environment or configuration files first

## When to Prompt

Prompt the user for credentials when:
- Setting up AWS services (AWS Access Key, Secret Key, Region)
- Configuring database connections (connection strings, passwords)
- Integrating third-party APIs (API keys, tokens)
- Setting up authentication systems (secrets, signing keys)
- Configuring email services (SMTP credentials)
- Any other service requiring authentication

## Best Practices

### Environment Variables
```python
import os

# Good: Use environment variables
api_key = os.environ.get('API_KEY')
database_url = os.environ.get('DATABASE_URL')

# Bad: Hardcoded credentials
api_key = "sk-1234567890abcdef"  # NEVER DO THIS
```

### Configuration Files
- Use `.env` files for local development (add to `.gitignore`)
- Use AWS Secrets Manager, Parameter Store, or similar for production
- Document required environment variables in README

### CDK/Infrastructure
```typescript
// Good: Reference from environment or context
const apiKey = process.env.API_KEY;

// Good: Use AWS Secrets Manager
const secret = secretsmanager.Secret.fromSecretNameV2(
  this, 'ApiKey', 'my-api-key'
);
```

## Prompt Template

When credentials are needed, ask the user:

```
I need to configure [SERVICE_NAME] which requires credentials.

Please provide:
- [CREDENTIAL_1]: [description]
- [CREDENTIAL_2]: [description]

Alternatively, I can:
1. Use environment variables (recommended)
2. Reference AWS Secrets Manager
3. Use configuration files (for local development only)

How would you like to proceed?
```

## Security Checklist

Before committing code, verify:
- [ ] No hardcoded credentials in source files
- [ ] Sensitive files added to `.gitignore`
- [ ] Environment variables documented in README
- [ ] Example configuration files use placeholder values
- [ ] No credentials in commit history

## Common Patterns

### AWS Credentials
```python
# Use boto3's credential chain (environment, ~/.aws/credentials, IAM role)
import boto3
client = boto3.client('s3')  # Automatically finds credentials
```

### Database URLs
```python
# Use environment variable
DATABASE_URL = os.environ.get('DATABASE_URL', 'sqlite:///./dev.db')
```

### API Keys
```python
# Use environment variable with validation
API_KEY = os.environ.get('API_KEY')
if not API_KEY:
    raise ValueError("API_KEY environment variable is required")
```

## Remember

**When in doubt, ask the user!** It's better to prompt for guidance than to make assumptions about credentials.
