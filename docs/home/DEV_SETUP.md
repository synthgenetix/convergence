# 🧪 Development Setup

This guide helps you set up Convergence for development and contribution.

## Development Environment

### Prerequisites

- Python 3.9+
- Git
- Docker (optional)
- OpenAI API Key

### Setup Development Environment

1. **Clone and Fork**
   ```bash
   git clone https://github.com/prodigaltech/convergence.git
   cd convergence
   ```

2. **Create Virtual Environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies**
   ```bash
   pip install -e ".[dev]"
   ```

4. **Setup Pre-commit Hooks**
   ```bash
   pre-commit install
   ```

## Code Quality Tools

### Linting

```bash
# Run linter
./scripts/lint.sh

# Auto-fix issues
./scripts/lint.sh --fix
```

### Type Checking

```bash
./scripts/typecheck.sh
```

### Security Scanning

```bash
./scripts/bandit.sh
```

### Running Tests

```bash
# Run all tests with coverage
./scripts/test.sh

# Run specific test file
pytest tests/test_generator.py -v
```

## Building

### Build Distribution

```bash
./scripts/build.sh
```

### Build Docker Image

```bash
docker build -t convergence:latest .
```

## Project Structure

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

## Design Principles

- **SOLID**: Clean architecture with separation of concerns
- **Self-Healing**: Automatic retry and fallback mechanisms
- **Environment-First**: Flexible configuration management
- **Type-Safe**: Full type hints with mypy validation

## Contributing Guidelines

### Code Style

- Follow PEP 8.
- Use type hints.
- Add docstrings to functions.
- Keep functions small and focused.

### Testing

- Write tests for new features.
- Maintain test coverage above 80%.
- Use pytest for testing.
- Mock external API calls.

### Commits

- Use conventional commit messages.
- Keep commits atomic.
- Reference issues in commits.

### Pull Requests

1. Fork the repository.
2. Create feature branch.
3. Make changes with tests.
4. Ensure all checks pass.
5. Submit PR with description.

## Development Tips

1. **Environment Variables**: Use `.env.local` for local overrides.
2. **Hot Reload**: Use `--reload` flag with uvicorn for API development.
3. **Debug Mode**: Set `DEBUG=true` in environment.
4. **Logging**: Check logs in `logs/` directory.

## Troubleshooting

- **Import Errors**: Ensure you're in the virtual environment.
- **API Key Issues**: Double-check your `.env` file.
- **Type Errors**: Run `mypy` to catch type issues.
- **Test Failures**: Check if you need to update mocks.

## Next Steps

- Read [Contributing](CONTRIBUTIONS) guidelines.
- Explore the [API documentation](API_USAGE).
- Check out [Features](FEATURES) for capabilities.