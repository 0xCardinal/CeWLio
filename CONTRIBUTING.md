# Contributing to CeWLio 🤝

Thank you for your interest in contributing to CeWLio! This document provides guidelines and instructions for contributors.

---

## 📋 Table of Contents

- [Getting Started](#getting-started)
- [Development Setup](#development-setup)
- [Code Style](#code-style)
- [Testing](#testing)
- [Submitting Changes](#submitting-changes)
- [Issue Reporting](#issue-reporting)
- [Feature Requests](#feature-requests)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.8 or higher
- Git
- pip (Python package installer)

### Fork and Clone

1. **Fork the repository** on GitHub
2. **Clone your fork** locally:
   ```bash
   git clone https://github.com/YOUR_USERNAME/cewlio.git
   cd cewlio
   ```
3. **Add the upstream remote**:
   ```bash
   git remote add upstream https://github.com/0xCardinal/cewlio.git
   ```

---

## 🔧 Development Setup

### 1. Install Dependencies

```bash
# Install the package in development mode with dev dependencies
pip install -e ".[dev]"

# Install Playwright browsers
playwright install
```

### 2. Verify Installation

```bash
# Test that the CLI works
cewlio --help

# Run the test suite
python -m unittest tests.test_cewlio -v
```

### 3. Development Environment

We recommend using a virtual environment:

```bash
# Create virtual environment
python -m venv venv

# Activate it (Unix/macOS)
source venv/bin/activate

# Activate it (Windows)
venv\Scripts\activate

# Install dependencies
pip install -e ".[dev]"
```

---

## 📝 Code Style

### Python Style Guide

We follow [PEP 8](https://www.python.org/dev/peps/pep-0008/) style guidelines:

- **Line length**: 88 characters (Black formatter)
- **Indentation**: 4 spaces (no tabs)
- **Naming conventions**:
  - `snake_case` for functions and variables
  - `PascalCase` for classes
  - `UPPER_CASE` for constants

### Code Formatting

We use [Black](https://black.readthedocs.io/) for code formatting:

```bash
# Format all Python files
black .

# Check formatting without making changes
black --check .
```

### Linting

We use [flake8](https://flake8.pycqa.org/) for linting:

```bash
# Run linter
flake8 cewlio/ tests/
```

### Type Checking

We use [mypy](https://mypy.readthedocs.io/) for type checking:

```bash
# Run type checker
mypy cewlio/
```

---

## 🧪 Testing

### Running Tests

```bash
# Run all tests
python -m unittest tests.test_cewlio -v

# Run specific test classes
python -m unittest tests.test_cewlio.TestCeWLio -v
python -m unittest tests.test_cewlio.TestCLIValidation -v
python -m unittest tests.test_cewlio.TestEdgeCases -v

# Run specific test methods
python -m unittest tests.test_cewlio.TestCeWLio.test_process_words_basic -v
```

### Test Structure

Our test suite is organized into several classes:

- **TestCeWLio**: Core functionality tests (15 tests)
- **TestExtractHTML**: HTML extraction tests (3 tests)
- **TestProcessURLWithCeWLio**: URL processing tests (2 tests)
- **TestIntegration**: Integration tests (3 tests)
- **TestCLIValidation**: CLI argument validation tests (5 tests)
- **TestEdgeCases**: Edge case tests (10 tests)

**Total: 38 tests with 100% success rate**

### Writing Tests

When adding new features, please include tests:

```python
def test_new_feature(self):
    """Test the new feature functionality."""
    cewlio = CeWLio()
    # Test setup
    result = cewlio.new_feature()
    # Assertions
    self.assertEqual(result, expected_value)
```

### Test Guidelines

- Write descriptive test method names
- Include docstrings explaining what the test does
- Test both success and failure cases
- Test edge cases and boundary conditions
- Keep tests independent and isolated

---

## 📦 Building and Packaging

### Build Package

```bash
# Install build tools
pip install build twine

# Build the package
python -m build
```

This creates:
- `dist/cewlio-1.0.0.tar.gz` (source distribution)
- `dist/cewlio-1.0.0-py3-none-any.whl` (wheel distribution)

### Test Installation

```bash
# Test installation from built package
pip install dist/cewlio-1.0.0-py3-none-any.whl

# Verify it works
cewlio --help
```

---

## 🔄 Submitting Changes

### 1. Create a Feature Branch

```bash
# Create and switch to a new branch
git checkout -b feature/your-feature-name

# Or for bug fixes
git checkout -b fix/your-bug-description
```

### 2. Make Your Changes

- Write your code following the style guidelines
- Add tests for new functionality
- Update documentation if needed
- Ensure all tests pass

### 3. Commit Your Changes

```bash
# Stage your changes
git add .

# Commit with a descriptive message
git commit -m "Add new feature: description of what was added"

# Push to your fork
git push origin feature/your-feature-name
```

### 4. Create a Pull Request

1. Go to your fork on GitHub
2. Click "New Pull Request"
3. Select your feature branch
4. Fill out the PR template
5. Submit the PR

### Commit Message Guidelines

Use conventional commit format:

```
type(scope): description

[optional body]

[optional footer]
```

Types:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation changes
- `style`: Code style changes (formatting, etc.)
- `refactor`: Code refactoring
- `test`: Adding or updating tests
- `chore`: Maintenance tasks

Examples:
```
feat(cli): add --no-words option to skip word extraction
fix(core): resolve umlaut conversion issue with single letters
docs(readme): update installation instructions
test(edge): add test for empty HTML processing
```

---

## 🐛 Issue Reporting

### Before Reporting

1. **Check existing issues** to see if your problem has already been reported
2. **Search the documentation** for solutions
3. **Try the latest version** to ensure the issue hasn't been fixed

### Creating an Issue

Use the appropriate issue template and include:

- **Clear title** describing the problem
- **Detailed description** of the issue
- **Steps to reproduce** the problem
- **Expected vs actual behavior**
- **Environment information**:
  - Operating system
  - Python version
  - CeWLio version
  - Browser version (if relevant)

### Example Issue

```
Title: CLI crashes when processing URLs with special characters

Description:
When running `cewlio https://example.com/path%20with%20spaces`, the CLI crashes with a URL encoding error.

Steps to reproduce:
1. Run: cewlio https://example.com/path%20with%20spaces
2. Observe crash

Expected behavior:
Should process the URL normally and extract words.

Actual behavior:
Crashes with: "UnicodeDecodeError: 'utf-8' codec can't decode byte..."

Environment:
- OS: macOS 14.0
- Python: 3.11.5
- CeWLio: 1.0.0
```

---

## 💡 Feature Requests

### Before Requesting

1. **Check existing issues** to see if the feature has been requested
2. **Consider the scope** - is this within CeWLio's purpose?
3. **Think about implementation** - is it feasible?

### Submitting a Feature Request

Include:

- **Clear description** of the feature
- **Use case** explaining why it's needed
- **Proposed implementation** (if you have ideas)
- **Alternatives considered** (if any)

### Example Feature Request

```
Title: Add support for extracting phone numbers

Description:
It would be useful to extract phone numbers from web pages, similar to how we extract emails.

Use case:
Security researchers often need phone numbers for social engineering assessments. Having them automatically extracted would save time.

Proposed implementation:
- Add phone number regex patterns
- Create PhoneExtractor class similar to EmailExtractor
- Add --phone option to CLI
- Store phone numbers in cewlio.phones set

Alternatives:
- Could use existing metadata extraction for phone numbers in meta tags
```

---

## 🏗️ Project Structure

```
cewlio/
├── cewlio/                    # Main package
│   ├── __init__.py           # Package exports
│   ├── core.py               # Main CeWLio class
│   ├── extractors.py         # HTML extraction logic
│   └── cli.py                # Command-line interface
├── tests/                    # Test suite
│   ├── test_cewlio.py        # Comprehensive tests
│   ├── README.md             # Test documentation
│   └── TEST_DOCUMENTATION.md # Detailed test docs
├── setup.py                  # Package setup
├── pyproject.toml           # Modern packaging config
├── requirements.txt         # Dependencies
├── CONTRIBUTING.md          # This file
└── README.md               # User documentation
```

### Key Files

- **`cewlio/core.py`**: Main CeWLio class with word processing logic
- **`cewlio/extractors.py`**: HTML extraction and browser automation
- **`cewlio/cli.py`**: Command-line interface
- **`tests/test_cewlio.py`**: Comprehensive test suite

---

## 🤝 Code Review Process

### Review Checklist

Before submitting a PR, ensure:

- [ ] Code follows style guidelines
- [ ] All tests pass
- [ ] New features have tests
- [ ] Documentation is updated
- [ ] No debugging code remains
- [ ] Commit messages are clear and descriptive

### Review Guidelines

When reviewing PRs:

- Be constructive and respectful
- Focus on the code, not the person
- Suggest improvements, don't just point out problems
- Test the changes locally if possible
- Consider edge cases and security implications

---

## 📚 Additional Resources

- [Python Style Guide (PEP 8)](https://www.python.org/dev/peps/pep-0008/)
- [Black Code Formatter](https://black.readthedocs.io/)
- [Flake8 Linter](https://flake8.pycqa.org/)
- [MyPy Type Checker](https://mypy.readthedocs.io/)
- [Conventional Commits](https://www.conventionalcommits.org/)

---

## 🎉 Recognition

Contributors will be recognized in:

- The project's README.md file
- Release notes
- GitHub contributors page

---

## 📞 Getting Help

If you need help with contributing:

- **GitHub Discussions**: [Start a discussion](https://github.com/0xCardinal/cewlio/discussions)
- **GitHub Issues**: [Open an issue](https://github.com/0xCardinal/cewlio/issues)
- **Documentation**: Check the [README.md](README.md) and test documentation

---

**Thank you for contributing to CeWLio! 🚀** 