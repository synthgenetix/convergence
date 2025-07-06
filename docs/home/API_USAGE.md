# 🌐 API Usage Guide

Convergence provides a RESTful API for integrating audio conversation generation into your applications.

## Starting the API Server

```bash
# Using uvicorn directly
uvicorn convergence.api.app:app --reload

# Or use Docker
docker-compose up
```

## API Endpoints

### Generate Audio Conversation

**Endpoint:** `POST /convergence/generate-audio`

#### Without Authentication

```bash
curl -X POST http://localhost:8000/convergence/generate-audio \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Two hackers discussing cybersecurity",
    "duration": 10,
    "vibe": "Technical and mysterious"
  }'
```

#### With Authentication Enabled

```bash
curl -X POST http://localhost:8000/convergence/generate-audio \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key-here" \
  -d '{
    "prompt": "Two hackers discussing cybersecurity",
    "duration": 10,
    "vibe": "Technical and mysterious"
  }'
```

#### With Outline URL

The API only accepts URLs for outlines (not file paths) for security reasons:

```bash
curl -X POST http://localhost:8000/convergence/generate-audio \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key-here" \
  -d '{
    "prompt": "Technical documentation review",
    "duration": 15,
    "vibe": "Professional and detailed",
    "outline_url": "https://raw.githubusercontent.com/user/repo/main/outline.md"
  }'
```

### Check Authentication Status

```bash
curl http://localhost:8000/auth/status
```

### Download Generated Audio

```bash
curl -O http://localhost:8000/convergence/download/convergence_audio_20240101_120000.wav
```

## Request Parameters

| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `prompt` | string | Yes | The conversation topic or scenario |
| `duration` | integer | No | Conversation length in minutes (default: 5) |
| `vibe` | string | No | The tone/style of the conversation |
| `outline_url` | string | No | URL to a document to guide the conversation |

## Response Format

The API returns a JSON response with:
- `status`: Success or error status.
- `audio_url`: URL to download the generated audio file.
- `metadata`: Information about the generated conversation.

## Cloud Version

**Note:** Send an email to contact.adityapatange@gmail.com for a demo API key when our Cloud version launches.

## Next Steps

- Learn about [API Key Management](API_KEY_MANAGEMENT.md) for securing your API.
- See [Self Hosting](SELF_HOST.md) for deployment options.
- Check the [SDK Usage](SDK_USAGE.md) for client integration examples.