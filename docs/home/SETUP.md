# 🚀 Setup Guide

This guide will help you get Convergence up and running on your system.

## Prerequisites

- Python 3.9+
- OpenAI API Key
- Docker (optional, for API deployment)

## Installation

### 1. Clone the Repository

```bash
git clone https://github.com/prodigaltech/convergence.git
cd convergence
```

### 2. Setup the CLI

```bash
chmod a+x setup_cli.sh
./setup_cli.sh
run # prints help and commands
```

### 3. Run the Setup Script

```bash
run setup
```

### 4. Configure Environment

```bash
cp .env.example .env
# Edit .env and add your OPENAI_API_KEY
```

## Environment Configuration

The system uses a hierarchical environment loading strategy:

1. `.env.{environment}` (e.g., `.env.production`)
2. `.env` (default)
3. `.env.local` (local overrides)

### Required Variables

```bash
OPENAI_API_KEY=your-api-key-here  # Required for transcript generation
ENVIRONMENT=development           # Optional: local/development/staging/production
```

## Next Steps

- Check out the [SDK Usage Guide](SDK_USAGE.md) for CLI examples.
- See [API Usage](API_USAGE.md) for REST API integration.
- Read about [Features](FEATURES.md) to understand all capabilities.