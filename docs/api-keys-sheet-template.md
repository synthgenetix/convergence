# 📊 API Keys Google Sheet Template

## Sheet Structure

Create a Google Sheet with the following columns:

| Column | Type | Description | Example |
|--------|------|-------------|---------|
| `api_key` | String | Unique API key | `sk-convergence-abc123xyz` |
| `client_name` | String | Name of the client/organization | `Acme Corporation` |
| `created_at` | ISO DateTime | When the key was created | `2024-01-01T00:00:00` |
| `expires_at` | ISO DateTime | When the key expires (optional) | `2024-12-31T23:59:59` |
| `is_active` | Boolean | Whether the key is active | `TRUE` |
| `rate_limit` | Integer | Requests per hour limit (optional) | `1000` |

## Example Data

```
api_key                     | client_name      | created_at           | expires_at           | is_active | rate_limit
---------------------------|------------------|---------------------|---------------------|-----------|------------
sk-convergence-prod-001    | Production App   | 2024-01-01T00:00:00 | 2024-12-31T23:59:59 | TRUE      | 5000
sk-convergence-dev-001     | Development Team | 2024-01-01T00:00:00 |                     | TRUE      | 1000
sk-convergence-test-001    | QA Testing       | 2024-01-01T00:00:00 | 2024-06-30T23:59:59 | TRUE      | 500
sk-convergence-demo-001    | Demo Account     | 2024-01-01T00:00:00 |                     | FALSE     | 100
```

## Setup Instructions

1. **Create a new Google Sheet**
   - Go to [Google Sheets](https://sheets.google.com)
   - Create a new spreadsheet
   - Name it appropriately (e.g., "Convergence API Keys")

2. **Add headers** (Row 1):
   - A1: `api_key`
   - B1: `client_name`
   - C1: `created_at`
   - D1: `expires_at`
   - E1: `is_active`
   - F1: `rate_limit`

3. **Configure sharing**:
   - Click "Share" button
   - Add your service account email (from the JSON key file)
   - Give "Viewer" permission (read-only access)

4. **Get the Sheet ID**:
   - Look at the URL: `https://docs.google.com/spreadsheets/d/{SHEET_ID}/edit`
   - Copy the `{SHEET_ID}` part
   - Add it to your `.env` file as `GOOGLE_SHEET_ID`

## Security Best Practices

1. **API Key Format**: Use a consistent prefix (e.g., `sk-convergence-`) for easy identification
2. **Expiration**: Set reasonable expiration dates for temporary keys
3. **Rate Limiting**: Configure appropriate rate limits based on client needs
4. **Regular Audits**: Periodically review and deactivate unused keys
5. **Access Control**: Only grant read access to the service account

## Troubleshooting

- **Authentication fails**: Ensure the service account has access to the sheet
- **Keys not loading**: Check that the sheet name matches `GOOGLE_SHEET_NAME` env var
- **Invalid date format**: Use ISO 8601 format: `YYYY-MM-DDTHH:MM:SS`