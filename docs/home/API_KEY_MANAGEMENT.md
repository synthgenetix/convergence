# 🔐 API Key Management

This guide explains how to set up and manage API key authentication for Convergence.

## Overview

When `AUTH_ENABLED=true`, the API requires authentication via API keys managed in Google Sheets. This provides:

- Centralized key management.
- Per-client rate limiting.
- Automatic expiration.
- Usage tracking.

## Setup

### 1. Create Google Sheet

Create a Google Sheet with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `api_key` | String | Unique API key (format: `sk-convergence-{unique-id}`) |
| `client_name` | String | Name of the client/application |
| `created_at` | DateTime | When the key was created |
| `expires_at` | DateTime | When the key expires (optional) |
| `is_active` | Boolean | Whether the key is currently active |
| `rate_limit` | Integer | Requests per minute allowed (optional) |

Example row:
```
api_key: sk-convergence-abc123xyz
client_name: MyApp Production
created_at: 2025-07-06 10:00:00
expires_at: 2025-12-31 23:59:59
is_active: TRUE
rate_limit: 60
```

### 2. Google Cloud Setup

1. **Create Service Account**
   - Go to Google Cloud Console.
   - Create a new service account.
   - Download the JSON key file.

2. **Share Sheet**
   - Open your Google Sheet.
   - Share with the service account email.
   - Grant "Editor" permissions.

### 3. Environment Configuration

```bash
# Enable API key authentication
AUTH_ENABLED=true

# Google Sheets configuration
GOOGLE_CREDENTIALS_PATH=/path/to/service-account-key.json
GOOGLE_SHEET_ID=your-google-sheet-id-here
GOOGLE_SHEET_NAME=API_Keys  # Default: API_Keys

# API key cache settings
API_KEY_CACHE_DURATION=300  # Cache duration in seconds (default: 300)
```

## Using API Keys

### Authentication Headers

The API accepts two header formats:

```bash
# Bearer token format
Authorization: Bearer sk-convergence-abc123xyz

# API key format
Authorization: ApiKey sk-convergence-abc123xyz
```

### Example Request

```bash
curl -X POST http://localhost:8000/convergence/generate-audio \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer sk-convergence-abc123xyz" \
  -d '{
    "prompt": "Two developers discussing API security",
    "duration": 10
  }'
```

## Security Features

### Automatic Expiration

- Keys are checked for expiration on each request.
- Expired keys are automatically rejected.
- No manual cleanup required.

### Rate Limiting

- Per-client rate limits based on `rate_limit` column.
- Returns 429 status when limit exceeded.
- Limits reset every minute.

### Client Identification

- Response headers include `X-Client-Name`.
- Useful for debugging and analytics.
- Helps track usage per client.

### Caching

- API keys are cached for performance.
- Default cache duration: 5 minutes.
- Configurable via `API_KEY_CACHE_DURATION`.

## Fallback Behavior

If authentication is enabled but Google credentials are missing:

1. Server starts in **unauthenticated mode**.
2. Warning is logged at startup.
3. All requests are allowed (no auth required).
4. `/auth/status` endpoint shows auth is disabled.

This ensures the service remains available even if authentication setup fails.

## Managing Keys

### Adding a New Key

1. Open your Google Sheet.
2. Add a new row with:
   - Generated API key (use a UUID generator).
   - Client name.
   - Current timestamp for created_at.
   - Set is_active to TRUE.

### Revoking a Key

1. Find the key in your Google Sheet.
2. Set `is_active` to FALSE.
3. Changes take effect after cache expires.

### Setting Expiration

1. Set `expires_at` to desired date/time.
2. Key will stop working after this time.
3. Leave empty for keys that never expire.

## Best Practices

### Key Format

Use consistent format for keys:
```
sk-convergence-{uuid}
```

Example:
```
sk-convergence-550e8400-e29b-41d4-a716-446655440000
```

### Security Tips

1. **Rotate Keys Regularly**: Set expiration dates.
2. **Limit Scope**: Create separate keys per environment.
3. **Monitor Usage**: Check logs for suspicious activity.
4. **Use HTTPS**: Always use SSL in production.
5. **Secure Storage**: Store keys in environment variables.

### Rate Limit Guidelines

- Development: 60 requests/minute
- Production: 300 requests/minute
- High-volume: Contact for custom limits

## Troubleshooting

### Common Issues

1. **"Authentication required" error**
   - Check AUTH_ENABLED setting.
   - Verify API key is included in header.
   - Ensure key is active in Google Sheet.

2. **"Invalid API key" error**
   - Verify key exists in Google Sheet.
   - Check is_active is TRUE.
   - Ensure key hasn't expired.

3. **"Rate limit exceeded" error**
   - Check rate_limit setting for client.
   - Wait for limit to reset (1 minute).
   - Consider requesting higher limit.

### Debug Mode

Enable debug logging to troubleshoot:
```bash
LOG_LEVEL=debug
```

This will show:
- Cache hits/misses.
- Google Sheets queries.
- Authentication decisions.

## Public Endpoints

These endpoints work without authentication:
- `/health` - Health check.
- `/auth/status` - Authentication status.

## Next Steps

- Review [Security Best Practices](SELF_HOST.md#security-considerations).
- Set up monitoring for API usage.
- Configure rate limits based on needs.