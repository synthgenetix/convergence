# 🤝 Contributing to Convergence

Convergence is a community project, built by developers for developers. We believe in the power of open source to bring people together and create amazing things.

## How to Contribute

### 1. Fork the Repository

```bash
# Fork on GitHub, then clone your fork
git clone https://github.com/YOUR_USERNAME/convergence.git
cd convergence

# Add upstream remote
git remote add upstream https://github.com/prodigaltech/convergence.git
```

### 2. Create Your Feature Branch

```bash
# Update your fork
git fetch upstream
git checkout main
git merge upstream/main

# Create feature branch
git checkout -b feature/amazing-feature
```

### 3. Make Your Changes

- Write clean, readable code.
- Add tests for new features.
- Update documentation.
- Follow existing code style.

### 4. Commit Your Changes

Use conventional commit messages:

```bash
# Format: <type>(<scope>): <subject>
git commit -m 'feat(audio): add support for multiple speakers'
git commit -m 'fix(api): handle empty prompt gracefully'
git commit -m 'docs(readme): update installation instructions'
```

Types:
- `feat`: New feature.
- `fix`: Bug fix.
- `docs`: Documentation.
- `style`: Code style changes.
- `refactor`: Code refactoring.
- `test`: Test additions/changes.
- `chore`: Maintenance tasks.

### 5. Push and Create PR

```bash
git push origin feature/amazing-feature
```

Then open a Pull Request on GitHub.

## Ideas for Contribution

### 🎨 Features

- **Web UI**: Build a React/Vue/Svelte interface.
- **Language Support**: Add multilingual capabilities.
- **Voice Cloning**: Integrate custom voice support.
- **Real-time Generation**: Stream audio as it's generated.
- **Conversation Templates**: Pre-built scenario templates.

### 🔧 Improvements

- **Performance**: Optimize generation speed.
- **Caching**: Implement smart caching strategies.
- **Error Handling**: Improve error messages and recovery.
- **Configuration**: Add more customization options.
- **Accessibility**: Make tools more accessible.

### 🧪 Testing & Quality

- **Test Coverage**: Increase coverage to 90%+.
- **Integration Tests**: Add end-to-end tests.
- **Performance Tests**: Benchmark generation times.
- **Documentation**: Improve code documentation.

### 🌍 Community

- **Examples**: Create example conversations.
- **Tutorials**: Write how-to guides.
- **Translations**: Translate documentation.
- **Bug Reports**: Report and fix bugs.
- **Feature Requests**: Suggest new features.

## Development Guidelines

### Code Style

```python
# Good: Clear, descriptive names
def generate_conversation_transcript(prompt: str, duration: int) -> dict:
    """Generate a conversation transcript from the given prompt."""
    pass

# Bad: Unclear abbreviations
def gen_conv(p, d):
    pass
```

### Testing

```python
# Write comprehensive tests
def test_conversation_generation():
    """Test that conversations are generated correctly."""
    result = generate_conversation("Test prompt", duration=5)
    assert result is not None
    assert len(result['items']) > 0
    assert all(item['message'] for item in result['items'])
```

### Documentation

- Add docstrings to all functions.
- Update README for new features.
- Create examples for complex features.
- Keep documentation up-to-date.

## Pull Request Process

1. **Ensure Quality**
   - All tests pass.
   - Code follows style guidelines.
   - Documentation is updated.

2. **Description**
   - Clearly describe what changes you made.
   - Reference any related issues.
   - Include screenshots for UI changes.

3. **Review**
   - Address reviewer feedback.
   - Be open to suggestions.
   - Keep discussions constructive.

4. **Merge**
   - Squash commits if requested.
   - Ensure branch is up-to-date.
   - Celebrate your contribution! 🎉

## Community Guidelines

### Be Respectful
- Welcome newcomers.
- Provide constructive feedback.
- Respect different perspectives.

### Be Helpful
- Answer questions.
- Share knowledge.
- Mentor new contributors.

### Be Inclusive
- Use inclusive language.
- Consider accessibility.
- Welcome diverse contributions.

## Recognition

All contributors will be:
- Listed in CONTRIBUTORS.md.
- Mentioned in release notes.
- Part of the Convergence community.

## Getting Help

- **Discord**: Join our community chat.
- **Issues**: Ask questions on GitHub.
- **Email**: contact.adityapatange@gmail.com.

## Remember

> "The best features come from weekend tinkering sessions!"

Every contribution, no matter how small, makes Convergence better. Whether it's fixing a typo, adding a feature, or sharing the project - you're part of something special.

Happy coding! 🚀