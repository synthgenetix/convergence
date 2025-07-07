# 🔥 Development Setup

This guide helps you set up Convergence for development and contribution.
Follow these steps to create a robust development environment that enables you to build new features, fix bugs, and contribute to the project effectively.

## 🔥 Development Environment

### 🔥 Prerequisites

- Python 3.9+ for modern language features and type hints.
  Install from python.org or use pyenv for version management.
- Git for version control and collaboration.
  Essential for cloning the repository and managing your contributions.
- Docker (optional) for containerized development and testing.
  Useful for testing deployment scenarios and ensuring consistency across environments.
- OpenAI API Key for accessing GPT and text-to-speech services.
  Sign up at platform.openai.com to get your API key for development.

### 🔥 Setup Development Environment

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

## 🔥 Code Quality Tools

### 🔥 Linting

```bash
# Run linter
./scripts/lint.sh

# Auto-fix issues
./scripts/lint.sh --fix
```

### 🔥 Type Checking

```bash
./scripts/typecheck.sh
```

### 🔥 Security Scanning

```bash
./scripts/bandit.sh
```

### 🔥 Running Tests

```bash
# Run all tests with coverage
./scripts/test.sh

# Run specific test file
pytest tests/test_generator.py -v
```

## 🔥 Building

### 🔥 Build Distribution

```bash
./scripts/build.sh
```

### 🔥 Build Docker Image

```bash
docker build -t convergence:latest .
```

## 🔥 Project Structure

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

## 🔥 Design Principles

- **SOLID**: Clean architecture with separation of concerns for maintainable code.
  Each component has a single responsibility, making the codebase easier to understand and modify.
- **Self-Healing**: Automatic retry and fallback mechanisms for robust operation.
  The system gracefully handles failures and recovers automatically when possible.
- **Environment-First**: Flexible configuration management for different deployment scenarios.
  Support for multiple environments with hierarchical configuration loading.
- **Type-Safe**: Full type hints with mypy validation for catching errors early.
  Comprehensive type annotations throughout the codebase prevent runtime type errors.

## 🔥 Contributing Guidelines

### 🔥 Code Style

- Follow PEP 8 for consistent Python code style.
  Use the provided linting tools to automatically check and fix style issues.
- Use type hints for all function signatures and variables.
  This improves code clarity and enables better IDE support and error detection.
- Add docstrings to functions following the Google style guide.
  Include descriptions of parameters, return values, and any exceptions raised.
- Keep functions small and focused on a single task.
  Functions should be easy to understand, test, and maintain.

### 🔥 Testing

- Write tests for new features before or alongside implementation.
  This ensures your code works correctly and prevents future regressions.
- Maintain test coverage above 80% to ensure code reliability.
  Use coverage reports to identify untested code paths and edge cases.
- Use pytest for testing with its powerful features and plugins.
  Leverage fixtures, parametrized tests, and marks for comprehensive test suites.
- Mock external API calls to ensure tests run quickly and reliably.
  Use pytest-mock or unittest.mock to isolate your tests from external dependencies.

### 🔥 Commits

- Use conventional commit messages for clear project history.
  Follow the format: type(scope): description for consistency.
- Keep commits atomic with one logical change per commit.
  This makes it easier to review changes and revert if necessary.
- Reference issues in commits using #issue-number syntax.
  This links commits to discussions and provides context for changes.

### 🔥 Pull Requests

1. Fork the repository to create your own copy for development.
   This allows you to experiment freely without affecting the main project.
2. Create feature branch with a descriptive name for your changes.
   Use the format feature/description or fix/issue-description.
3. Make changes with tests to ensure your code works correctly.
   Write tests first (TDD) or alongside your implementation.
4. Ensure all checks pass including linting, type checking, and tests.
   Run the provided scripts to verify your code meets all quality standards.
5. Submit PR with description explaining your changes and motivation.
   Include screenshots for UI changes and reference any related issues.

## 🔥 Development Tips

1. **Environment Variables**: Use `.env.local` for local overrides that won't be committed.
   This keeps your personal settings separate from the shared configuration.
2. **Hot Reload**: Use `--reload` flag with uvicorn for API development efficiency.
   Changes to your code will automatically restart the server for rapid iteration.
3. **Debug Mode**: Set `DEBUG=true` in environment for detailed logging.
   This provides verbose output that helps diagnose issues during development.
4. **Logging**: Check logs in `logs/` directory for debugging information.
   Logs are organized by date and include detailed error traces when issues occur.

## 🔥 Troubleshooting

- **Import Errors**: Ensure you're in the virtual environment before running code.
  Activate the venv with `source venv/bin/activate` or use the correct Python interpreter.
- **API Key Issues**: Double-check your `.env` file for correct formatting.
  Ensure the key is properly quoted and the variable name matches exactly.
- **Type Errors**: Run `mypy` to catch type issues before runtime.
  Address any type inconsistencies to maintain code quality.
- **Test Failures**: Check if you need to update mocks for API changes.
  External API responses may have changed, requiring mock updates.

## 🔥 Next Steps

- Read [Contributing](CONTRIBUTIONS) guidelines for detailed contribution process.
  Learn about our code of conduct, commit conventions, and review process.
- Explore the [API documentation](API_USAGE) to understand endpoints.
  Familiarize yourself with the API structure for building integrations.
- Check out [Features](FEATURES) for capabilities and roadmap.
  Understand what Convergence can do and where it's heading.