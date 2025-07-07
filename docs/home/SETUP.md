# 🔥 Setup Guide

Get Convergence running in minutes with this comprehensive setup guide.
Whether you're using pip or setting up for development, we'll guide you through every step of the installation process.

## 🔥 Prerequisites

- **Python 3.9+** ([Download](https://www.python.org/downloads/)).
  Python is the foundation of Convergence, and version 3.9 or higher ensures compatibility with all modern features.
- **OpenAI API Key** ([Get one](https://platform.openai.com/api-keys)).
  You'll need this key to access the AI models that power the conversation generation.
- **Docker** (optional, for API deployment).
  Docker simplifies deployment and ensures consistency across different environments.

## 🔥 Quick Install

```bash
pip install convergence
```

This single command installs Convergence and all its dependencies.
The package is regularly updated on PyPI with the latest features and improvements.

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

This key enables Convergence to communicate with OpenAI's language models.
Keep this key secure and never commit it to version control.

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
OPENAI_API_KEY=your-api-key-here  # Required for AI model access.
ENVIRONMENT=development           # Optional, defaults to 'development'.
```

## 🔥 Verify Installation

```bash
python -m convergence --help
```

This command displays all available options and confirms that Convergence is properly installed.
You should see a comprehensive help menu with all CLI commands and parameters.

## 🔥 Next Steps

- [**SDK Usage**](SDK_USAGE) - Learn CLI commands and explore all available options.
  Master the command-line interface to generate conversations with custom parameters.
- [**API Usage**](API_USAGE) - REST API integration for building applications.
  Discover how to integrate Convergence into your own applications using our RESTful API.
- [**Features**](FEATURES) - Explore capabilities and discover what Convergence can do.
  Learn about all the powerful features available for generating synthetic audio conversations.