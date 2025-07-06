# CeWLio Test Suite

This directory contains a comprehensive test suite for CeWLio functionality using Python's unittest framework.

## Test Files

- **`test_cewlio.py`** - Main test suite with comprehensive unittest-based tests
- **`run_tests.py`** - Test runner for executing tests with various options
- **`TEST_DOCUMENTATION.md`** - Detailed documentation of all test cases
- **`README.md`** - This file

## Test Coverage

The test suite provides **complete coverage** of all CeWLio features:

### Core Functionality (100%)
- ✅ Word extraction and processing
- ✅ Email address extraction (including mailto links)
- ✅ Metadata extraction from HTML meta tags
- ✅ HTML cleaning and processing
- ✅ File output functionality

### Configuration Options (100%)
- ✅ Minimum/maximum word length filtering
- ✅ Lowercase conversion
- ✅ Words with numbers inclusion
- ✅ Umlaut conversion (ä→ae, ö→oe, ü→ue, ß→ss)
- ✅ Word count display
- ✅ Word group generation
- ✅ No-words mode (only emails/metadata)

### Edge Cases (100%)
- ✅ Empty HTML input
- ✅ HTML with only comments
- ✅ HTML with only script tags
- ✅ Very long words
- ✅ Special characters
- ✅ Invalid email formats
- ✅ Network errors and timeouts

### Integration (100%)
- ✅ Complete end-to-end workflows
- ✅ File I/O operations
- ✅ Error handling
- ✅ Async operations with Playwright

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install -r requirements.txt
```

Install Playwright browsers:
```bash
playwright install
```

### Run All Tests
```bash
python run_tests.py
```

### Run Specific Test Categories
```bash
# Core CeWLio functionality
python run_tests.py --class cewlio

# HTML extraction tests
python run_tests.py --class extract_html

# URL processing tests
python run_tests.py --class process_url

# Integration tests
python run_tests.py --class integration

# Edge case tests
python run_tests.py --class edge_cases
```

### Run Specific Test Methods
```bash
# Test email extraction (including mailto fix)
python run_tests.py --test test_extract_emails_mailto

# Test word length filtering
python run_tests.py --test test_process_words_length_filtering

# Test umlaut conversion
python run_tests.py --test test_process_words_convert_umlauts

# Test metadata extraction
python run_tests.py --test test_extract_metadata
```

### List Available Tests
```bash
python run_tests.py --list
```

### Show Help
```bash
python run_tests.py --help
```

## Test Structure

### TestCeWLio Class
Tests the core CeWLio class functionality:

- **Initialization Tests** - Default and custom parameter initialization
- **HTML Processing Tests** - HTML cleaning, metadata extraction, complete processing
- **Word Processing Tests** - Basic extraction, case conversion, numbers, umlauts, length filtering, groups
- **Email Extraction Tests** - Standard patterns and mailto links
- **Output Tests** - Words, counts, emails, metadata, console output

### TestExtractHTML Class
Tests HTML extraction functionality:

- **Success scenarios** - Normal HTML extraction
- **Wait time handling** - Extraction with delays
- **Failure scenarios** - Network errors and timeouts

### TestProcessURLWithCeWLio Class
Tests URL processing workflows:

- **Success scenarios** - Complete URL processing
- **Failure scenarios** - Error handling and recovery

### TestIntegration Class
Tests complete integration workflows:

- **End-to-end workflows** - Full processing pipelines
- **Word groups integration** - Group generation in workflows
- **File output integration** - File I/O in complete scenarios

### TestEdgeCases Class
Tests edge cases and error conditions:

- **Empty content** - Empty HTML, comments only, scripts only
- **Special content** - Very long words, special characters
- **Conversion edge cases** - Umlaut conversion edge cases
- **Email edge cases** - Invalid email formats and edge cases

## Key Test Features

### Email Extraction Fix
The test suite specifically validates the mailto link fix:
```python
def test_extract_emails_mailto(self):
    """Test email extraction from mailto links."""
    text = '<a href="mailto:contact@example.com">Contact</a>'
    emails = self.cewlio.extract_emails(text)
    self.assertIn("contact@example.com", emails)
```

### Comprehensive Coverage
- **Unit tests** for individual components
- **Integration tests** for complete workflows
- **Edge case tests** for error conditions
- **Mock tests** for external dependencies

### Real-world Scenarios
Tests use realistic HTML content including:
- Meta tags (description, keywords, author)
- Email addresses (text and mailto links)
- Various HTML structures
- Special characters and edge cases

## Test Results

When all tests pass, you should see output like:
```
Ran 25 tests in 2.5s
OK
```

## Adding New Tests

To add new tests:

1. Add test methods to the appropriate test class in `test_cewlio.py`
2. Follow the naming convention: `test_<feature_name>()`
3. Use descriptive docstrings explaining what the test validates
4. Include both positive and negative test cases
5. Update `TEST_DOCUMENTATION.md` with new test descriptions

## Test Requirements

- Tests should be self-contained and independent
- Use descriptive test names and docstrings
- Include both success and failure scenarios
- Mock external dependencies appropriately
- Clean up any temporary files created during tests
- Use realistic test data that represents actual usage 