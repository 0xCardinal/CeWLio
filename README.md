# CeWLio 🕵️‍♂️✨

**CeWLio** is a powerful, Python-based Custom Word List Generator inspired by the original [CeWL](https://digi.ninja/projects/cewl.php) by Robin Wood. It crawls web pages, executes JavaScript, and extracts:

- 📚 Unique words (with advanced filtering)
- 📧 Email addresses
- 🏷️ Metadata (description, keywords, author)

Perfect for penetration testers, security researchers, and anyone needing high-quality, site-specific wordlists!

---

## 🚀 Features

- **JavaScript-Aware Extraction:** Uses a headless browser to render pages and extract content after JavaScript execution.
- **Flexible Word Filtering:**
  - Minimum/maximum word length
  - Lowercase conversion
  - Alphanumeric or alpha-only
  - Umlaut conversion (ä→ae, ö→oe, etc.)
- **Word Grouping:** Generate multi-word phrases (e.g., 2-grams, 3-grams).
- **Email & Metadata Extraction:** Find emails and meta tag content.
- **Custom Output:** Save words, emails, and metadata to separate files.
- **CLI Power:** All features accessible via command-line arguments.

---

## 🛠️ Installation

1. **Clone the repo:**
   ```bash
   git clone https://github.com/0xCardinal/cewlio
   cd cewlio
   ```
2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

---

## ⚡ Usage

```bash
python cpp.py <url> [options]
```

### Examples

- Basic wordlist from a site:
  ```bash
  python cewl.py https://example.com
  ```
- Save wordlist to a file:
  ```bash
  python cewl.py https://example.com -o wordlist.txt
  ```
- Extract emails and save to a file:
  ```bash
  python cewl.py https://example.com -e --email-file emails.txt
  ```
- Generate 3-word phrases, only lowercase, min 4/max 10 chars:
  ```bash
  python cewl.py https://example.com -g 3 --lowercase -m 4 -x 10
  ```
- Set custom timeout (60 seconds):
  ```bash
  python cewl.py https://example.com -t 60000
  ```
- Save everything to separate files:
  ```bash
  python cewl.py https://example.com -o words.txt -e --email-file emails.txt -a --metadata-file meta.txt
  ```
---

## 🎛️ Command-Line Options

| Option                | Description                                  |
|-----------------------|----------------------------------------------|
| `url`                 | URL to process                               |
| `-o, --output`        | Output file for wordlist                     |
| `--email-file`        | Output file for email addresses              |
| `--metadata-file`     | Output file for metadata                     |
| `-m, --min-word-length` | Minimum word length (default: 3)           |
| `-x, --max-word-length` | Maximum word length                        |
| `--lowercase`         | Convert all words to lowercase               |
| `--with-numbers`      | Include words with numbers                   |
| `--convert-umlauts`   | Convert umlauts (ä→ae, etc.)                 |
| `-g, --groups`        | Generate word groups of specified size       |
| `-c, --count`         | Show word count                             |
| `-w, --wait`          | Wait time (seconds) after page load         |
| `--visible`           | Run browser in visible mode                  |
| `-t, --timeout`       | Timeout (ms) for page load (default: 30000) |
| `-e, --email`         | Extract email addresses                      |
| `-a, --metadata`      | Extract metadata                             |
| `--no-words`          | Don't extract words (only emails/metadata)   |

---

## 🧩 How It Works

1. Loads the target URL in a headless browser (with JS support)
2. Extracts and cleans HTML, including text from attributes
3. Finds words, emails, and metadata
4. Outputs results to console or files

---

## 📝 Credits

- Inspired by [CeWL](https://digi.ninja/projects/cewl.php) by Robin Wood

---

## 📄 License

MIT License 