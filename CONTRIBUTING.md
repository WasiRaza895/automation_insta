# Contributing to Instagram Automation System

Thank you for your interest in contributing! This document provides guidelines for contributing to this project.

## 🤝 How to Contribute

### Reporting Issues
- Check existing issues before creating a new one
- Use clear, descriptive titles
- Include steps to reproduce bugs
- Include your environment details (OS, Python version, etc.)

### Suggesting Features
- Open an issue with the "enhancement" label
- Clearly describe the feature and its use case
- Explain why it would be valuable

### Submitting Pull Requests

1. **Fork the Repository**
   ```bash
   git clone https://github.com/yourusername/automation_insta.git
   cd automation_insta
   ```

2. **Create a Branch**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **Make Your Changes**
   - Follow the existing code style
   - Add comments for complex logic
   - Update documentation if needed

4. **Test Your Changes**
   ```bash
   python test_setup.py
   python demo.py
   ```

5. **Commit Your Changes**
   ```bash
   git commit -m "Add feature: description of changes"
   ```

6. **Push and Create PR**
   ```bash
   git push origin feature/your-feature-name
   ```
   Then open a Pull Request on GitHub

## 📋 Code Standards

### Python Style
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and small

### Documentation
- Update README.md for user-facing changes
- Add inline comments for complex logic
- Include examples for new features

### Testing
- Test changes locally before submitting
- Ensure existing tests still pass
- Add tests for new features when possible

## 🔧 Development Setup

1. **Clone and Install**
   ```bash
   git clone https://github.com/WasiRaza895/automation_insta.git
   cd automation_insta
   pip install -r requirements.txt
   ```

2. **Set Up Environment**
   ```bash
   cp .env.example .env
   # Edit .env with your credentials
   ```

3. **Run Tests**
   ```bash
   python test_setup.py
   python demo.py
   ```

## 🎯 Priority Areas

We especially welcome contributions in these areas:
- **Video Enhancement**: Better text styling, animations, transitions
- **Content Quality**: Improved prompt engineering for better quotes
- **Instagram Features**: Support for Stories, Carousels, etc.
- **Safety**: Better rate limiting, block detection, proxy support
- **Analytics**: Track post performance, engagement metrics
- **Testing**: Unit tests, integration tests
- **Documentation**: Tutorials, examples, troubleshooting guides

## 🐛 Found a Security Issue?

Please **do not** open a public issue. Instead, email the maintainer directly with details.

## 📜 Code of Conduct

- Be respectful and inclusive
- Provide constructive feedback
- Focus on the issue, not the person
- Help others learn and grow

## ❓ Questions?

- Open an issue with the "question" label
- Check existing issues and discussions
- Read the documentation thoroughly first

Thank you for contributing! 🎉
