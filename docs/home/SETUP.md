# 🚀 Setup Guide

```{note}
This guide will help you get Convergence up and running on your system in just a few minutes!
```

## Prerequisites

```{important}
Before you begin, ensure you have the following:
```

- **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
- **OpenAI API Key** - [Get your API key](https://platform.openai.com/api-keys)
- **Docker** (optional) - For API deployment

## Installation

```{admonition} Quick Install
:class: tip

For the fastest setup, you can use pip:
```bash
pip install convergence
```
```

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

```{grid} 3
:gutter: 2

```{grid-item-card} SDK Usage
:link: SDK_USAGE
:link-type: doc
Learn CLI commands and examples
```

```{grid-item-card} API Usage
:link: API_USAGE
:link-type: doc
Integrate with REST API
```

```{grid-item-card} Features
:link: FEATURES  
:link-type: doc
Explore all capabilities
```
```