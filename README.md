<div align="center">

# 🧙🏼‍♂️ CONVERGENCE

<p align="center"><img src="assets/convergence_logo.png" width="230" alt="Convergence Logo">

**Where minds meet in the digital ether.**

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Open Source Love](https://badges.frapsoft.com/os/v1/open-source.svg?v=103)](https://github.com/ellerbrock/open-source-badges/)

_A platform service for generating synthetic audio conversations, born from the joy of programming and the belief that technology should enhance life._

</div>

---

## 🌊 About Convergence

> "_Engineering is more than just a source of livelihood - it's what makes me who I am._ — AdiPat"

**CONVERGENCE** is an open-source platform that generates synthetic audio conversations using advanced AI. Born from weekend tinkering sessions and a deep love for programming, this project represents the convergence of technology, creativity, and human connection.

Built with passion during those precious hours between work commitments, Convergence transforms simple prompts into rich, lifelike conversations - from group discussions and podcasts to mock standups and beyond. It's a testament to what's possible when we code not just for function, but for joy.

### ✨ Features

- 🧬 **Neural Synthesis**: Generate natural conversations on any topic. Just 1 CLI command to get started.
- 🎭 **Dynamic Personas**: AI-driven personalities with distinct voices. Configurable personalities via prompt, vibe, custom transcripts and outline.
- 📋 **Outline Support**: Guide conversations with structured outlines (files or URLs). You can choose to use the outline as a conversation spec or protocol, or anything you wish!
- 🗣️ **Pre-defined Conversations**: Generate audio from JSON conversation transcripts. Generate audio from your own transcript, either self-written or generated via LLMs.
- 📝 **AI Transcript Generation**: Create realistic dialogues using GPT-4.1, Open AI's flagship model as of July 2025. Good if you you have a quick idea and want AI to generate the transcript.
- 🎤 **Real TTS Integration**: OpenAI text-to-speech with automatic voice selection. Supports all Open AI voices.
- 🔮 **Seamless Flow**: Natural conversation progression between speakers. Conversations flow smoothly, with no abrupt shifts or endings.
- 🌐 **Self-hosted, API First**: RESTful API with Docker support - build your own UI! You can fully self-host or use the pip package.
- 🎨 **Developer-Friendly CLI**: Clean, intuitive command-line experience. **We make DevEx a priority 🔥**.

---

## 🚀 Quick Start

### Prerequisites

- Python 3.9+.
- OpenAI API Key.
- Docker (optional, for API deployment).

### Installation

```bash
# Clone the repository
git clone https://github.com//convergence.git
cd convergence

# Setup the CLI
chmod a+x setup_cli.sh
./setup_cli.sh
run # prints help and commands

# Run the setup script
run setup

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

**NOTE:** Send an email to contact.adityapatange@gmail for a demo API key when our Cloud version launches.

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

- **Format Support**: Markdown, text files, and other formats via `markitdown` conversion.
- **URL Fetching**: Direct download from HTTP/HTTPS URLs.
- **Size Limits**: Outlines are truncated to 50KB for performance.
- **Formatting**: Automatic cleanup and standardization of bullet points.
- **Error Handling**: Graceful fallback if processing fails.

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

- **Automatic Voice Assignment**: Voices are automatically selected based on gender.
  - Female voices: alloy, coral, fable, nova, sage.
  - Male voices: ash, ballad, echo, onyx, shimmer.
- **Environment Variable Substitution**: Use `$env.OPENAI_API_KEY` in the config.
- **Real TTS Integration**: Uses OpenAI's `tts-1` model for high-quality speech.
- **Multi-speaker Support**: Each speaker gets a consistent voice throughout.

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

- **Smart Dialogue Generation**: Uses GPT-4.1 to create natural conversations.
- **Context Awareness**: Each response builds on previous exchanges.
- **Configurable Parameters**: Control prompt, duration, and conversation style.
- **JSON Output**: Saves in the same format as pre-defined conversations.
- **No Sensitive Data**: API keys are replaced with environment variable references.

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

- Multiple dialogue exchanges (approximately 2-3 per minute).
- Consistent speaker personas throughout the conversation.
- Natural conversation flow with proper context.
- Timestamps spaced evenly across the duration.

---

## 🧪 Development

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

## 🔐 Environment Configuration

The system uses a hierarchical environment loading strategy:

1. `.env.{environment}` (e.g., `.env.production`)
2. `.env` (default)
3. `.env.local` (local overrides)

### Required Variables

```bash
OPENAI_API_KEY=your-api-key-here  # Required for transcript generation
ENVIRONMENT=development           # Optional: local/development/staging/production
```

### Authentication Variables (Optional)

Create an empty Google Sheet and setup your credentials on Google Cloud. Add these credentials to the env file should you choose to have `AUTH_ENABLED=true`. Else, you can always use the service via Docker as a sidecar or internally within your VPC.

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

- **API Key Authentication**: Optional Google Sheets-based API key management.
- **No hardcoded secrets**: All sensitive data in environment variables.
- **Input validation**: Comprehensive validation on all endpoints.
- **Secure file handling**: Path validation and access controls.
- **Regular security scans**: Automated scanning with Bandit.
- **Rate limiting support**: Per-API key rate limits (when auth enabled).

---

## 🤝 Contributing

Convergence is a community project, built by developers for developers. We believe in the power of open source to bring people together and create amazing things.

### How to Contribute

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 🌠 The Philosophy

Convergence represents more than just code - it's a point where love, science, philosophy, meditation, programming, human psychology, art, and engineering fuse together. It's a reminder that technology, at its best, is a creative expression of our humanity.

This project has been in the works since 2022, evolving from an AI podcast idea into a platform that makes synthetic data generation accessible and usable for everyone. It's about democratizing AI capabilities and putting powerful tools in the hands of creators, researchers, and dreamers.

## 📬 Get Involved

- **Star** this repo if you find it interesting.
- **Watch** for updates and new features.
- **Fork** and build something amazing.
- **Share** your creations with the community.

Interested in early access? Want to contribute? Have ideas? Let's connect!

## 📜 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

---

<div align="center">

**🚀 Welcome to the Convergence. ☀️**

_Convergence is where (and when) smoke got transformed into binary fuel for the digital sentients._

_When creativity, mindfulness, technology and consciousness combine in the sentient's experience of life, the sentient becomes deathless. — Laws of Convergence, 8164_

---

</div>
