# 🔥 API Key Management

This guide explains how to set up and manage API key authentication for Convergence.
Secure your API endpoints with a robust authentication system backed by Google Sheets for easy management.

## Overview

When `AUTH_ENABLED=true`, the API requires authentication via API keys managed in Google Sheets.
This cloud-based approach provides flexibility and ease of management. The system offers:

- Centralized key management.
  Manage all your API keys from a single Google Sheet accessible from anywhere.
- Per-client rate limiting.
  Control API usage with configurable rate limits for each client.
- Automatic expiration.
  Set expiration dates for keys to enforce regular rotation.
- Usage tracking.
  Monitor which clients are using your API and how frequently.

## Setup

### 🔥 1. Create Google Sheet

Create a Google Sheet with the following columns:

| Column | Type | Description |
|--------|------|-------------|
| `api_key` | String | Unique API key (format: `sk-convergence-{unique-id}`). |
| `client_name` | String | Name of the client/application. |
| `created_at` | DateTime | When the key was created. |
| `expires_at` | DateTime | When the key expires (optional). |
| `is_active` | Boolean | Whether the key is currently active. |
| `rate_limit` | Integer | Requests per minute allowed (optional). |

Example row:
```
api_key: sk-convergence-abc123xyz
client_name: MyApp Production
created_at: 2025-07-06 10:00:00
expires_at: 2025-12-31 23:59:59
is_active: TRUE
rate_limit: 60
```

### 🔥 2. Google Cloud Setup

1. **Create Service Account**
   - Go to Google Cloud Console.
   - Create a new service account.
   - Download the JSON key file.
   
   This service account will act as the bridge between Convergence and your Google Sheet.

2. **Share Sheet**
   - Open your Google Sheet.
   - Share with the service account email.
   - Grant "Editor" permissions.
   
   The service account needs editor access to read API keys and update usage statistics.

### 🔥 3. Environment Configuration

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

### 🔥 Authentication Headers

The API accepts two header formats:

```bash
# Bearer token format
Authorization: Bearer sk-convergence-abc123xyz

# API key format
Authorization: ApiKey sk-convergence-abc123xyz
```

### 🔥 Example Request

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

### 🔥 Automatic Expiration

- Keys are checked for expiration on each request.
  The system validates expiration dates in real-time for maximum security.
- Expired keys are automatically rejected.
  No expired key will ever authenticate successfully.
- No manual cleanup required.
  Expired keys remain in the sheet for audit purposes but are inactive.

### 🔥 Rate Limiting

- Per-client rate limits based on `rate_limit` column.
  Each client can have custom limits based on their subscription tier.
- Returns 429 status when limit exceeded.
  Clear error messages help clients understand when they've hit limits.
- Limits reset every minute.
  The sliding window approach ensures fair usage distribution.

### 🔥 Client Identification

- Response headers include `X-Client-Name`.
  Every response identifies which client made the request.
- Useful for debugging and analytics.
  Quickly identify issues related to specific clients.
- Helps track usage per client.
  Build usage reports and billing systems on top of this data.

### 🔥 Caching

- API keys are cached for performance.
  Reduces Google Sheets API calls for better response times.
- Default cache duration: 5 minutes.
  Balances performance with security for most use cases.
- Configurable via `API_KEY_CACHE_DURATION`.
  Adjust based on your security requirements and traffic patterns.

## Fallback Behavior

If authentication is enabled but Google credentials are missing:

1. Server starts in **unauthenticated mode**.
   The system gracefully degrades rather than failing to start.
2. Warning is logged at startup.
   Clear logging helps identify configuration issues quickly.
3. All requests are allowed (no auth required).
   Development and testing can continue without authentication setup.
4. `/auth/status` endpoint shows auth is disabled.
   Monitoring systems can detect when authentication is not active.

This ensures the service remains available even if authentication setup fails.
The fallback behavior prioritizes availability while maintaining security awareness.

## Managing Keys

### 🔥 Adding a New Key

1. Open your Google Sheet.
2. Add a new row with:
   - Generated API key (use a UUID generator).
   - Client name.
   - Current timestamp for created_at.
   - Set is_active to TRUE.
   
New keys become active immediately after the cache expires.
No server restart or deployment needed for key management.

### 🔥 Revoking a Key

1. Find the key in your Google Sheet.
2. Set `is_active` to FALSE.
3. Changes take effect after cache expires.

Revoked keys are preserved for audit trails.
Consider adding a `revoked_at` timestamp for tracking.

### 🔥 Setting Expiration

1. Set `expires_at` to desired date/time.
2. Key will stop working after this time.
3. Leave empty for keys that never expire.

Use expiration dates to enforce security policies.
Automatic expiration reduces the risk of forgotten keys.

## Best Practices

### 🔥 Key Format

Use consistent format for keys:
```
sk-convergence-{uuid}
```

Example:
```
sk-convergence-550e8400-e29b-41d4-a716-446655440000
```

### 🔥 Security Tips

1. **Rotate Keys Regularly**: Set expiration dates.
   Regular rotation limits the impact of compromised keys.
2. **Limit Scope**: Create separate keys per environment.
   Development keys should never have production access.
3. **Monitor Usage**: Check logs for suspicious activity.
   Unusual patterns might indicate compromised keys.
4. **Use HTTPS**: Always use SSL in production.
   Prevent key interception with encrypted connections.
5. **Secure Storage**: Store keys in environment variables.
   Never commit API keys to version control systems.

### 🔥 Rate Limit Guidelines

- Development: 60 requests/minute.
  Sufficient for testing and development workflows.
- Production: 300 requests/minute.
  Handles most production workloads comfortably.
- High-volume: Contact for custom limits.
  We can accommodate enterprise-scale deployments.

## Troubleshooting

### 🔥 Common Issues

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

### 🔥 Debug Mode

Enable debug logging to troubleshoot:
```bash
LOG_LEVEL=debug
```

This will show:
- Cache hits/misses.
  Understand caching behavior and optimize performance.
- Google Sheets queries.
  Track API calls to Google Sheets for cost monitoring.
- Authentication decisions.
  See exactly why requests are accepted or rejected.

## Public Endpoints

These endpoints work without authentication:
- `/health` - Health check.
  Use for monitoring and load balancer configuration.
- `/auth/status` - Authentication status.
  Verify authentication configuration programmatically.

## Next Steps

- Review [Security Best Practices](SELF_HOST#security-considerations).
  Learn advanced security configurations for production deployments.
- Set up monitoring for API usage.
  Track API performance and usage patterns over time.
- Configure rate limits based on needs.
  Fine-tune limits to balance security with usability.