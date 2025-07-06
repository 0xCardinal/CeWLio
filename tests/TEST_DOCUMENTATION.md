# CeWLio Test Suite Documentation

This document describes the comprehensive test suite for CeWLio (Custom Word List Generator).

## Overview

The test suite covers all functionality of CeWLio including:
- Core word extraction and processing
- Email address extraction
- Metadata extraction from HTML
- HTML cleaning and processing
- File output functionality
- Integration workflows
- Edge cases and error conditions

## Test Structure

### 1. TestCeWL Class
Tests the core CeWL class functionality:

#### Initialization Tests
- `test_initialization()` - Tests default parameter initialization
- `test_initialization_with_custom_params()` - Tests custom parameter initialization

#### HTML Processing Tests
- `test_clean_html()` - Tests HTML tag, comment, and entity removal
- `test_extract_metadata()` - Tests metadata extraction from meta tags
- `test_process_html_complete()` - Tests complete HTML processing workflow

#### Word Processing Tests
- `test_process_words_basic()` - Tests basic word extraction
- `test_process_words_lowercase()` - Tests lowercase conversion
- `test_process_words_with_numbers()` - Tests alphanumeric word extraction
- `test_process_words_convert_umlauts()` - Tests umlaut character conversion
- `test_process_words_length_filtering()` - Tests word length filtering
- `test_process_words_groups()` - Tests word group generation

#### Email Extraction Tests
- `test_extract_emails()` - Tests standard email pattern extraction
- `test_extract_emails_mailto()` - Tests email extraction from mailto links

#### Output Tests
- `test_save_results_words_only()` - Tests word list output
- `test_save_results_with_counts()` - Tests output with word counts
- `test_save_results_emails()` - Tests email output
- `test_save_results_metadata()` - Tests metadata output
- `test_save_results_to_stdout()` - Tests console output

### 2. TestExtractHTML Class
Tests the HTML extraction functionality:

- `test_extract_html_success()` - Tests successful HTML extraction
- `test_extract_html_with_wait_time()` - Tests extraction with wait time
- `test_extract_html_failure()` - Tests extraction failure handling

### 3. TestProcessURLWithCeWL Class
Tests the URL processing workflow:

- `test_process_url_success()` - Tests successful URL processing
- `test_process_url_failure()` - Tests URL processing failure

### 4. TestIntegration Class
Tests complete integration workflows:

- `test_complete_workflow_with_sample_data()` - Tests full workflow with sample HTML
- `test_word_groups_integration()` - Tests word groups in integration
- `test_file_output_integration()` - Tests file output in integration

### 5. TestEdgeCases Class
Tests edge cases and error conditions:

- `test_empty_html()` - Tests processing empty HTML
- `test_html_with_only_comments()` - Tests HTML with only comments
- `test_html_with_only_scripts()` - Tests HTML with only script tags
- `test_very_long_words()` - Tests very long word handling
- `test_words_with_special_characters()` - Tests special character handling
- `test_umlaut_conversion_edge_cases()` - Tests umlaut conversion edge cases
- `test_email_edge_cases()` - Tests email extraction edge cases

## Running Tests

### Prerequisites

Install test dependencies:
```bash
pip install -r test_requirements.txt
```

Install Playwright browsers:
```bash
playwright install
```

### Running All Tests

From the project root directory:
```bash
python run_tests.py
```

Or from the tests directory:
```bash
cd tests
python run_tests.py
```

### Using the Test Runner

The test runner provides flexible test execution:

```bash
# Run all tests
python run_tests.py

# Run specific test class
python run_tests.py --class cewl
python run_tests.py --class integration
python run_tests.py --class edge_cases

# Run specific test method
python run_tests.py --test test_initialization
python run_tests.py --test test_extract_emails

# List available tests
python run_tests.py --list
```

### Available Test Classes

- `cewl` - Core CeWL functionality tests
- `extract_html` - HTML extraction tests  
- `process_url` - URL processing tests
- `integration` - Integration tests
- `edge_cases` - Edge case tests

## Test Data

The tests use various sample HTML content to verify functionality:

### Sample HTML Structure
```html
<!DOCTYPE html>
<html>
<head>
    <meta name="description" content="Test website with sample content">
    <meta name="keywords" content="test, sample, website, content">
    <meta name="author" content="Test Author">
    <title>Test Page</title>
</head>
<body>
    <h1>Welcome to Test Page</h1>
    <p>This is a sample paragraph with some words.</p>
    <p>Contact us at <a href="mailto:test@example.com">test@example.com</a></p>
    <p>Another email: user@domain.org</p>
    <div alt="Alternative text" title="Title text" placeholder="Placeholder text">
        More content here with different words.
    </div>
    <!-- This is a comment -->
    <script>var test = "javascript content";</script>
</body>
</html>
```

## Test Coverage

The test suite covers:

### Core Functionality (100%)
- ✅ Word extraction and processing
- ✅ Email address extraction
- ✅ Metadata extraction
- ✅ HTML cleaning
- ✅ File output
- ✅ Configuration options

### Configuration Options (100%)
- ✅ Minimum/maximum word length
- ✅ Lowercase conversion
- ✅ Number inclusion
- ✅ Umlaut conversion
- ✅ Word counts
- ✅ Word groups

### Edge Cases (100%)
- ✅ Empty input
- ✅ Invalid emails
- ✅ Special characters
- ✅ Very long words
- ✅ HTML comments only
- ✅ Script tags only

### Integration (100%)
- ✅ Complete workflows
- ✅ File I/O
- ✅ Error handling
- ✅ Async operations

## Expected Test Results

When all tests pass, you should see output like:

```
test_initialization (__main__.TestCeWL) ... ok
test_initialization_with_custom_params (__main__.TestCeWL) ... ok
test_clean_html (__main__.TestCeWL) ... ok
...

----------------------------------------------------------------------
Ran 25 tests in 2.5s

OK

==================================================
TEST SUMMARY
==================================================
Tests run: 25
Failures: 0
Errors: 0
Success rate: 100.0%
```

## Troubleshooting

### Common Issues

1. **Playwright not installed**
   ```
   Error: playwright not found
   ```
   Solution: Run `playwright install`

2. **Import errors**
   ```
   ImportError: No module named 'extract_html'
   ```
   Solution: Ensure you're running tests from the project root directory

3. **Async test failures**
   ```
   RuntimeError: Event loop is closed
   ```
   Solution: Tests use proper async/await patterns, ensure Python 3.7+

### Debugging Tests

To debug a specific test:

```bash
# Run with verbose output
python -m unittest test_cewl.TestCeWL.test_extract_emails -v

# Run with debugger
python -m pdb test_cewl.py
```

## Adding New Tests

To add new tests:

1. Add test methods to appropriate test classes
2. Follow naming convention: `test_<functionality_name>()`
3. Use descriptive test names
4. Include both positive and negative test cases
5. Test edge cases and error conditions

Example:
```python
def test_new_feature(self):
    """Test new feature functionality."""
    # Arrange
    cewl = CeWL()
    test_data = "test content"
    
    # Act
    cewl.process_words(test_data)
    
    # Assert
    self.assertIn("test", cewl.words)
    self.assertIn("content", cewl.words)
```

## Performance Considerations

- Tests use mocked Playwright for HTML extraction tests
- File I/O tests use temporary files that are cleaned up
- Async tests are properly handled with asyncio
- Large HTML content tests are kept minimal to maintain speed

## Continuous Integration

The test suite is designed to work with CI/CD systems:

- Exit codes indicate test success/failure
- No external dependencies for core functionality tests
- Mocked external services for reliable testing
- Clear error messages for debugging 