# API Usage Guide

Convergence provides a RESTful API for integrating audio conversation generation into your applications.
This powerful API enables you to programmatically generate synthetic conversations, making it perfect for automation, integrations, and building custom user interfaces.

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

The API only accepts URLs for outlines (not file paths) for security reasons.
This design choice prevents unauthorized file system access and ensures that only publicly accessible content can be used as conversation guides.

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
| `prompt` | string | Yes | The conversation topic or scenario. |
| `duration` | integer | No | Conversation length in minutes (default: 5). |
| `vibe` | string | No | The tone/style of the conversation. |
| `outline_url` | string | No | URL to a document to guide the conversation. |

## Response Format

The API returns a JSON response with comprehensive information about your generated conversation.
This structured response makes it easy to handle the results programmatically in your applications.
- `status`: Success or error status indicating whether the generation completed successfully.
  Check this field first to determine if you should process the response or handle an error.
- `audio_url`: URL to download the generated audio file in high-quality WAV format.
  This URL provides direct access to your generated conversation audio for streaming or downloading.
- `metadata`: Information about the generated conversation including duration and parameters.
  Use this data to track generations, display information to users, or store for analytics.

## Cloud Version

**Note:** Send an email to contact.adityapatange@gmail.com for a demo API key when our Cloud version launches.
Our cloud service will provide hassle-free access to Convergence without the need for self-hosting or managing infrastructure.

## Next Steps

- Learn about [API Key Management](API_KEY_MANAGEMENT) for securing your API endpoints.
  Implement proper authentication to control access and track usage across different clients.
- See [Self Hosting](SELF_HOST) for deployment options in your own infrastructure.
  Explore various deployment strategies from Docker containers to Kubernetes clusters.
- Check the [SDK Usage](SDK_USAGE) for client integration examples and best practices.
  Learn how to use Convergence from various programming languages and frameworks.