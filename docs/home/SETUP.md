# Setup Guide

Get Convergence running in minutes.

## Prerequisites

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **OpenAI API Key** ([Get one](https://platform.openai.com/api-keys))
- **Docker** (optional, for API deployment)

## Quick Install

```bash
pip install convergence
```

## Development Setup

### 1. Clone Repository

```bash
git clone https://github.com/prodigaltech/convergence.git
cd convergence
```

### 2. Setup CLI

```bash
chmod a+x setup_cli.sh
./setup_cli.sh
run setup
```

### 3. Configure Environment

```bash
cp .env.example .env
```

Add your OpenAI API key to `.env`:
```bash
OPENAI_API_KEY=your-api-key-here
```

## Environment Variables

Convergence uses hierarchical environment loading:

1. `.env.{environment}` (e.g., `.env.production`)
2. `.env` (default)
3. `.env.local` (local overrides)

### Essential Variables

```bash
OPENAI_API_KEY=your-api-key-here  # Required
ENVIRONMENT=development           # Optional
```

## Verify Installation

```bash
python -m convergence --help
```

## Next Steps

- [**SDK Usage**](SDK_USAGE.md) - Learn CLI commands
- [**API Usage**](API_USAGE.md) - REST API integration
- [**Features**](FEATURES.md) - Explore capabilities