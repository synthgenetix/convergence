# 🔥 Setup Guide

Get Convergence running in minutes with this comprehensive setup guide.
Whether you're using pip or setting up for development, we'll guide you through every step of the installation process.

## 🔥 Prerequisites

- **Python 3.9+** ([Download](https://www.python.org/downloads/))
- **OpenAI API Key** ([Get one](https://platform.openai.com/api-keys))
- **Docker** (optional, for API deployment)

## 🔥 Quick Install

```bash
pip install convergence
```

## 🔥 Development Setup

### 🔥 1. Clone Repository

```bash
git clone https://github.com/prodigaltech/convergence.git
cd convergence
```

### 🔥 2. Setup CLI

```bash
chmod a+x setup_cli.sh
./setup_cli.sh
run setup
```

### 🔥 3. Configure Environment

```bash
cp .env.example .env
```

Add your OpenAI API key to `.env`:
```bash
OPENAI_API_KEY=your-api-key-here
```

## 🔥 Environment Variables

Convergence uses hierarchical environment loading for flexible configuration management.
This system allows you to maintain different settings for development, staging, and production environments.

1. `.env.{environment}` (e.g., `.env.production`) - Environment-specific settings that override defaults.
   Use this for production API keys, database connections, and environment-specific configurations.
2. `.env` (default) - Base configuration file with common settings across all environments.
   This file contains your standard configuration that applies unless overridden by environment-specific files.
3. `.env.local` (local overrides) - Personal settings that should never be committed to version control.
   Perfect for developer-specific configurations and temporary testing values.

### 🔥 Essential Variables

```bash
OPENAI_API_KEY=your-api-key-here  # Required
ENVIRONMENT=development           # Optional
```

## 🔥 Verify Installation

```bash
python -m convergence --help
```

## 🔥 Next Steps

- [**SDK Usage**](SDK_USAGE) - Learn CLI commands and explore all available options.
  Master the command-line interface to generate conversations with custom parameters.
- [**API Usage**](API_USAGE) - REST API integration for building applications.
  Discover how to integrate Convergence into your own applications using our RESTful API.
- [**Features**](FEATURES) - Explore capabilities and discover what Convergence can do.
  Learn about all the powerful features available for generating synthetic audio conversations.