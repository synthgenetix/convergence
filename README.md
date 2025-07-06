# 🌌 CONVERGENCE

<div align="center">

```
╔═══════════════════════════════════════════════════════════════╗
║  ▄████▄   ▒█████   ███▄    █ ██▒   █▓▓█████  ██▀███    ▄████ ║
║ ▒██▀ ▀█  ▒██▒  ██▒ ██ ▀█   █▓██░   █▒▓█   ▀ ▓██ ▒ ██▒ ██▒ ▀█▒║
║ ▒▓█    ▄ ▒██░  ██▒▓██  ▀█ ██▒▓██  █▒░▒███   ▓██ ░▄█ ▒▒██░▄▄▄░║
║ ▒▓▓▄ ▄██▒▒██   ██░▓██▒  ▐▌██▒ ▒██ █░░▒▓█  ▄ ▒██▀▀█▄  ░▓█  ██▓║
║ ▒ ▓███▀ ░░ ████▓▒░▒██░   ▓██░  ▒▀█░  ░▒████▒░██▓ ▒██▒░▒▓███▀▒║
║ ░ ░▒ ▒  ░░ ▒░▒░▒░ ░ ▒░   ▒ ▒   ░ ▐░  ░░ ▒░ ░░ ▒▓ ░▒▓░ ░▒   ▒ ║
║   ░  ▒     ░ ▒ ▒░ ░ ░░   ░ ▒░  ░ ░░   ░ ░  ░  ░▒ ░ ▒░  ░   ░ ║
╚═══════════════════════════════════════════════════════════════╝
```

**🎭 AI-Powered Audio Conversation Generator 🎵**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

</div>

---

## 🌊 Overview

**CONVERGENCE** is a cutting-edge AI system that generates realistic audio conversations between synthetic personas. Using advanced language models and audio synthesis, it creates immersive dialogues that blur the line between human and machine communication.

### ✨ Features

- 🧬 **Neural Synthesis**: Generate natural conversations on any topic
- 🎭 **Dynamic Personas**: AI-driven personalities with distinct voices
- 📋 **Outline Support**: Guide conversations with structured outlines (files or URLs)
- 🗣️ **Pre-defined Conversations**: Generate audio from JSON conversation transcripts
- 📝 **AI Transcript Generation**: Create realistic dialogues using GPT-4
- 🎤 **Real TTS Integration**: OpenAI text-to-speech with automatic voice selection
- 🔮 **Quantum Entanglement**: Seamless conversation flow between speakers
- 🛡️ **Self-Healing**: Automatic fallback mechanisms for robust operation
- 🌐 **API First**: RESTful API with Docker support
- 🎨 **Sci-Fi CLI**: Immersive command-line experience
- 🔄 **Format Conversion**: Automatic conversion of various file formats to markdown

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+
- OpenAI API Key
- Docker (optional, for API deployment)

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/convergence.git
cd convergence

# Run the setup script
chmod +x scripts/setup.sh
./scripts/setup.sh

# Configure your environment
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

### 🎯 CLI Usage

```bash
# Generate a conversation
python -m convergence --prompt "Two friends discussing quantum computing" \
                     --duration 10 \
                     --vibe "Enthusiastic and technical" \
                     --output output/quantum_talk.wav

# With custom environment file
python -m convergence --prompt "AI consciousness debate" \
                     --duration 15 \
                     --env .env.production \
                     --vibe "Philosophical and deep"

# With outline file or URL
python -m convergence --prompt "Technical deep dive on AI" \
                     --duration 20 \
                     --outline /path/to/outline.md \
                     --vibe "Educational and structured"

# Using online outline
python -m convergence --prompt "Product review discussion" \
                     --outline https://example.com/product-outline.md \
                     --duration 15

# Using pre-defined conversation JSON
python -m convergence --conversation ./data/test_conversation_01.json \
                     --output data/test.wav

# Generate conversation transcript using AI
python -m convergence --generate-transcript \
                     --prompt "Two engineers discussing cloud architecture" \
                     --duration 5 \
                     --vibe "Professional and thoughtful"

# Generate transcript with defaults
python -m convergence --generate-transcript
```

### 🌐 API Usage

```bash
# Start the API server
uvicorn convergence.api.app:app --reload

# Or use Docker
docker-compose up
```

#### API Endpoints

```bash
# Generate audio conversation (without auth)
curl -X POST http://localhost:8000/convergence/generate-audio \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Two hackers discussing cybersecurity",
    "duration": 10,
    "vibe": "Technical and mysterious"
  }'

# Generate audio conversation (with auth enabled)
curl -X POST http://localhost:8000/convergence/generate-audio \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key-here" \
  -d '{
    "prompt": "Two hackers discussing cybersecurity",
    "duration": 10,
    "vibe": "Technical and mysterious"
  }'

# With outline URL (API only accepts URLs, not file paths)
curl -X POST http://localhost:8000/convergence/generate-audio \
  -H "Content-Type: application/json" \
  -H "Authorization: Bearer your-api-key-here" \
  -d '{
    "prompt": "Technical documentation review",
    "duration": 15,
    "vibe": "Professional and detailed",
    "outline_url": "https://raw.githubusercontent.com/user/repo/main/outline.md"
  }'

# Check authentication status
curl http://localhost:8000/auth/status

# Download generated audio
curl -O http://localhost:8000/convergence/download/convergence_audio_20240101_120000.wav
```

#### 🔐 API Authentication

When `AUTH_ENABLED=true`, the API requires authentication via API keys managed in Google Sheets:

1. **Google Sheets Setup**:
   - Create a Google Sheet with columns: `api_key`, `client_name`, `created_at`, `expires_at`, `is_active`, `rate_limit`
   - Share the sheet with your service account email
   - Add API keys in the format: `sk-convergence-{unique-id}`

2. **Authentication Headers**:
   - Use `Authorization: Bearer {api-key}` or `Authorization: ApiKey {api-key}`
   - API keys are cached for performance (default: 5 minutes)

3. **Security Features**:
   - Automatic expiration checking
   - Per-client rate limiting
   - Client identification in response headers (`X-Client-Name`)

4. **Startup Behavior**:
   - If auth is enabled but Google credentials are missing, the server starts in **unauthenticated mode** with a warning
   - The `/health` and `/auth/status` endpoints remain public

---

## 📋 Outline Feature

The outline feature allows you to guide conversations with structured content, making the generated dialogue more focused and relevant.

### CLI Usage

The CLI accepts both local files and URLs via the `--outline` or `-u` parameter:

```bash
# Local markdown file
python -m convergence --prompt "AI ethics discussion" \
                     --outline ./outlines/ai-ethics.md

# URL to online document
python -m convergence --prompt "Product review" \
                     --outline https://example.com/product-spec.md

# Non-markdown files are automatically converted
python -m convergence --prompt "Technical documentation" \
                     --outline ./docs/spec.pdf
```

### API Usage

The API only accepts URLs for security reasons:

```json
{
  "prompt": "Technical review",
  "duration": 15,
  "vibe": "Professional",
  "outline_url": "https://raw.githubusercontent.com/user/repo/main/outline.md"
}
```

### Supported Features

- **Format Support**: Markdown, text files, and other formats via `markitdown` conversion
- **URL Fetching**: Direct download from HTTP/HTTPS URLs
- **Size Limits**: Outlines are truncated to 50KB for performance
- **Formatting**: Automatic cleanup and standardization of bullet points
- **Error Handling**: Graceful fallback if outline processing fails

---

## 🗣️ Pre-defined Conversations

The conversation feature allows you to generate audio from pre-defined conversation transcripts, using OpenAI's text-to-speech API with automatic voice assignment.

### JSON Format

Create a conversation JSON file with the following structure:

```json
{
  "transcript": {
    "items": [
      {
        "name": "Alice",
        "gender": "female",
        "role": "Developer",
        "message": "Hey Bob, did you see the new release?",
        "timestamp": "2025-07-07T10:00:00"
      },
      {
        "name": "Bob",
        "gender": "male", 
        "role": "Engineer",
        "message": "Yeah! It's amazing!",
        "timestamp": "2025-07-07T10:00:05"
      }
    ]
  },
  "config": {
    "prompt": "Two colleagues discussing tech",
    "duration": 5,
    "vibe": "Excited",
    "output_path": "output/tech_talk.wav",
    "openai_api_key": "$env.OPENAI_API_KEY"
  }
}
```

### Features

- **Automatic Voice Assignment**: Voices are automatically selected based on gender
  - Female voices: alloy, coral, fable, nova, sage
  - Male voices: ash, ballad, echo, onyx, shimmer
- **Environment Variable Substitution**: Use `$env.OPENAI_API_KEY` in the config
- **Real TTS Integration**: Uses OpenAI's `tts-1` model for high-quality speech
- **Multi-speaker Support**: Each speaker gets a consistent voice throughout

### Usage

```bash
# Generate audio from conversation JSON
python -m convergence --conversation ./data/conversation.json

# Override output path
python -m convergence --conversation ./data/conversation.json \
                     --output custom_output.wav
```

---

## 📝 AI Transcript Generation

Generate realistic conversation transcripts using OpenAI's language models. The generated transcripts can then be converted to audio.

### Features

- **Smart Dialogue Generation**: Uses GPT-4 to create natural conversations
- **Context Awareness**: Each response builds on previous exchanges
- **Configurable Parameters**: Control prompt, duration, and conversation style
- **JSON Output**: Saves in the same format as pre-defined conversations
- **No Sensitive Data**: API keys are replaced with environment variable references

### Usage

```bash
# Generate with specific parameters
python -m convergence --generate-transcript \
                     --prompt "Two scientists discussing quantum computing" \
                     --duration 5 \
                     --vibe "Academic and curious"

# Use defaults (casual tech conversation)
python -m convergence --generate-transcript

# Generate then convert to audio (two-step process)
python -m convergence --generate-transcript --duration 3
python -m convergence --conversation output/conversation_[timestamp].json
```

### Generated Format

The transcript generator creates JSON files with:
- Multiple dialogue exchanges (approximately 2-3 per minute)
- Consistent speaker personas throughout the conversation
- Natural conversation flow with proper context
- Timestamps spaced evenly across the duration

---

## 🧪 Development

### Running Tests

```bash
# Run all tests with coverage
./scripts/test.sh

# Run specific test file
pytest tests/test_generator.py -v
```

### Code Quality

```bash
# Run linter
./scripts/lint.sh

# Auto-fix issues
./scripts/lint.sh --fix

# Type checking
./scripts/typecheck.sh

# Security scan
./scripts/bandit.sh
```

### Building

```bash
# Build distribution
./scripts/build.sh

# Build Docker image
docker build -t convergence:latest .
```

---

## 🏗️ Architecture

```
convergence/
├── core/               # 🧠 Core business logic
│   ├── generator.py    # Main conversation generator
│   └── models.py       # Data models
├── services/           # ⚙️ Service layer
│   ├── transcript.py   # Transcript generation
│   └── audio.py        # Audio synthesis
├── api/                # 🌐 FastAPI application
│   ├── app.py          # API configuration
│   └── routes.py       # API endpoints
├── utils/              # 🛠️ Utilities
│   ├── console.py      # CLI aesthetics
│   └── env.py          # Environment management
└── __main__.py         # 🚀 CLI entry point
```

### Design Principles

- **SOLID**: Clean architecture with separation of concerns
- **Self-Healing**: Automatic retry and fallback mechanisms
- **Environment-First**: Flexible configuration management
- **Type-Safe**: Full type hints with mypy validation

---

## 🔐 Environment Configuration

The system uses a hierarchical environment loading strategy:

1. `.env.{environment}` (e.g., `.env.production`)
2. `.env` (default)
3. `.env.local` (local overrides)

### Required Variables

```bash
OPENAI_API_KEY=your-api-key-here  # Required for transcript generation
ENVIRONMENT=development           # Optional: development/staging/production
```

### Authentication Variables (Optional)

```bash
# Enable API key authentication
AUTH_ENABLED=true

# Google Sheets configuration for API key management
GOOGLE_CREDENTIALS_PATH=/path/to/service-account-key.json
GOOGLE_SHEET_ID=your-google-sheet-id-here
GOOGLE_SHEET_NAME=API_Keys  # Default: API_Keys

# API key cache settings
API_KEY_CACHE_DURATION=300  # Cache duration in seconds (default: 300)
```

---

## 🛡️ Security

- **API Key Authentication**: Optional Google Sheets-based API key management
- **No hardcoded secrets**: All sensitive data in environment variables
- **Input validation**: Comprehensive validation on all endpoints
- **Secure file handling**: Path validation and access controls
- **Regular security scans**: Automated scanning with Bandit
- **Rate limiting support**: Per-API key rate limits (when auth enabled)

---

## 🤝 Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**🌌 Welcome to the Convergence 🌌**

*Where minds meet in the digital ether*

</div> 
