# CeWLio 🕵️‍♂️✨

[![AI-Assisted Development](https://img.shields.io/badge/AI--Assisted-Development-blue?style=for-the-badge&logo=openai&logoColor=white)](https://github.com/0xCardinal/cewlio)
[![Python](https://img.shields.io/badge/Python-3.12+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![License](https://img.shields.io/badge/License-MIT-green?style=for-the-badge)](LICENSE)
[![Tests](https://img.shields.io/badge/Tests-Passed-brightgreen?style=for-the-badge)](CONTRIBUTING.md#testing)

**CeWLio** is a powerful, Python-based Custom Word List Generator inspired by the original [CeWL](https://digi.ninja/projects/cewl.php) by Robin Wood. While CeWL is excellent for static HTML content, CeWLio brings modern web scraping capabilities to handle today's JavaScript-heavy websites. It crawls web pages, executes JavaScript, and extracts:

- 📚 Unique words (with advanced filtering)
- 📧 Email addresses  
- 🏷️ Metadata (description, keywords, author)

Perfect for penetration testers, security researchers, and anyone needing high-quality, site-specific wordlists!

> **🤖 AI-Assisted Development**: This project was created with the help of AI tools, but solves real-world problems in web scraping and word list generation. Every line of code has been carefully reviewed, tested, and optimized for production use.

---

## 🚀 Features

- **JavaScript-Aware Extraction:** Uses headless browser to render pages and extract content after JavaScript execution.
- **Modern Web Support:** Handles Single Page Applications (SPAs), infinite scroll, lazy loading, and dynamic content that traditional scrapers miss.
- **Advanced Word Processing:**
  - Minimum/maximum word length filtering
  - Lowercase conversion
  - Alphanumeric or alpha-only words
  - Umlaut conversion (ä→ae, ö→oe, ü→ue, ß→ss)
  - Word frequency counting
- **Word Grouping:** Generate multi-word phrases (e.g., 2-grams, 3-grams)
- **Email & Metadata Extraction:** Find emails from content and mailto links, extract meta tags
- **Flexible Output:** Save words, emails, and metadata to separate files or stdout
- **Professional CLI:** All features accessible via command-line interface with CeWL-compatible flags
- **Silent Operation:** Runs quietly by default, with optional debug output
- **Comprehensive Testing:** 100% test coverage

---

## 🛠️ Installation

### From PyPI (Recommended)
```bash
pip install cewlio
```

### From Source
```bash
git clone https://github.com/0xCardinal/cewlio
cd cewlio
pip install -e .
```

### Dependencies
- Python 3.12+
- Playwright (for browser automation)
- BeautifulSoup4 (for HTML parsing)
- Requests (for HTTP handling)

---

## ⚡ Quick Start

### Basic Usage
```bash
# Extract words from a website (silent by default)
cewlio https://example.com

# Save words to a file
cewlio https://example.com --output wordlist.txt

# Include emails in stdout output
cewlio https://example.com -e

# Include metadata in stdout output
cewlio https://example.com -a

# Save emails and metadata to files
cewlio https://example.com --email_file emails.txt --meta_file meta.txt
```

### More Examples

**Generate word groups with counts:**
```bash
cewlio https://example.com --groups 3 -c --output phrases.txt
```

**Custom word filtering:**
```bash
cewlio https://example.com -m 4 --max-length 12 --lowercase --convert-umlauts
```

**Handle JavaScript-heavy sites:**
```bash
cewlio https://example.com -w 5 --visible
```

**Extract only emails and metadata (no words):**
```bash
cewlio https://example.com -e -a
```

**Extract only emails (no words):**
```bash
cewlio https://example.com -e
```

**Extract only metadata (no words):**
```bash
cewlio https://example.com -a
```

**Save emails to file (no words to stdout):**
```bash
cewlio https://example.com --email_file emails.txt
```

---

## 🎛️ Command-Line Options

| Option | Description | Default |
|--------|-------------|---------|
| `url` | URL to process | Required |
| `--version` | Show version and exit | - |
| `--output` | Output file for words | stdout |
| `-e, --email` | Include email addresses in stdout output | False |
| `--email_file` | Output file for email addresses | - |
| `-a, --meta` | Include metadata in stdout output | False |
| `--meta_file` | Output file for metadata | - |
| `-m, --min_word_length` | Minimum word length | 3 |
| `--max-length` | Maximum word length | No limit |
| `--lowercase` | Convert words to lowercase | False |
| `--with-numbers` | Include words with numbers | False |
| `--convert-umlauts` | Convert umlaut characters | False |
| `-c, --count` | Show word counts | False |
| `--groups` | Generate word groups of specified size | - |
| `-w, --wait` | Wait time for JavaScript execution (seconds) | 0 |
| `--visible` | Show browser window | False |
| `--timeout` | Browser timeout (milliseconds) | 30000 |
| `--debug` | Show debug/summary output | False |

---

## 📚 API Usage

### Basic Python Usage
```python
from cewlio import CeWLio

# Create instance with custom settings
cewlio = CeWLio(
    min_word_length=4,
    max_word_length=12,
    lowercase=True,
    convert_umlauts=True
)

# Process HTML content
html_content = "<p>Hello world! Contact us at test@example.com</p>"
cewlio.process_html(html_content)

# Access results
print("Words:", list(cewlio.words.keys()))
print("Emails:", list(cewlio.emails))
print("Metadata:", list(cewlio.metadata))
```

### Process URLs
```python
import asyncio
from cewlio import CeWLio, process_url_with_cewlio

async def main():
    cewlio = CeWLio()
    success = await process_url_with_cewlio(
        url="https://example.com",
        cewlio_instance=cewlio,
        wait_time=5,
        headless=True
    )
    
    if success:
        print(f"Found {len(cewlio.words)} words")
        print(f"Found {len(cewlio.emails)} emails")

asyncio.run(main())
```

---

## 🧪 Testing

The project includes a comprehensive test suite with 33 tests covering all functionality:

- ✅ Core functionality tests (15 tests)
- ✅ HTML extraction tests (3 tests)  
- ✅ URL processing tests (2 tests)
- ✅ Integration tests (3 tests)
- ✅ Edge case tests (10 tests)

**Total: 33 tests with 100% success rate**

For detailed testing information and development setup, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 🐛 Troubleshooting

### Common Issues

**"No module named 'playwright'"**
```bash
pip install playwright
playwright install
```

**JavaScript-heavy sites not loading properly**
```bash
# Increase wait time for JavaScript execution
cewlio https://example.com -w 10
```

**Browser timeout errors**
```bash
# Increase timeout and wait time
cewlio https://example.com --timeout 60000 -w 5
```

---

## 🤝 Contributing

We welcome contributions! Please see [CONTRIBUTING.md](CONTRIBUTING.md) for detailed guidelines on:

- 🚀 Getting started with development
- 📝 Code style and formatting guidelines
- 🧪 Testing requirements and procedures
- 🔄 Submitting pull requests
- 🐛 Reporting issues
- 💡 Feature requests

Quick start:
1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests for new functionality
5. Submit a pull request

For detailed development setup and guidelines, see [CONTRIBUTING.md](CONTRIBUTING.md).

---

## 🙏 Credits

- Inspired by [CeWL](https://digi.ninja/projects/cewl.php) by Robin Wood
- Built with [Playwright](https://playwright.dev/) for browser automation
- Uses [BeautifulSoup4](https://www.crummy.com/software/BeautifulSoup/) for HTML parsing

---

## 📞 Support

- 🐛 **Issues:** [GitHub Issues](https://github.com/0xCardinal/cewlio/issues)
- 📖 **Documentation:** [GitHub Wiki](https://github.com/0xCardinal/cewlio/wiki)
- 💬 **Discussions:** [GitHub Discussions](https://github.com/0xCardinal/cewlio/discussions)

---

**Made with ❤️ for the security community** 
