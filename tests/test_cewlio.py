#!/usr/bin/env python3
"""
Comprehensive test suite for CeWLio (Custom Word List Generator)
Tests all functionality including word extraction, email extraction, metadata extraction,
HTML processing, and various configuration options.
"""

import unittest
import tempfile
import os
import asyncio
from unittest.mock import patch, MagicMock, AsyncMock
from io import StringIO
import sys

# Import the modules to test
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from cewlio import CeWLio, process_url_with_cewlio
from cewlio.extractors import extract_html


class TestCeWLio(unittest.TestCase):
    """Test cases for the CeWLio class functionality."""
    
    def setUp(self):
        """Set up test fixtures."""
        self.cewlio = CeWLio()
        self.sample_html = """
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
        """

    def test_initialization(self):
        """Test CeWLio initialization with default parameters."""
        cewlio = CeWLio()
        self.assertEqual(cewlio.min_word_length, 3)
        self.assertIsNone(cewlio.max_word_length)
        self.assertFalse(cewlio.lowercase)
        self.assertFalse(cewlio.with_numbers)
        self.assertFalse(cewlio.convert_umlauts)
        self.assertFalse(cewlio.show_count)
        self.assertEqual(len(cewlio.words), 0)
        self.assertEqual(len(cewlio.emails), 0)
        self.assertEqual(len(cewlio.metadata), 0)

    def test_initialization_with_custom_params(self):
        """Test CeWLio initialization with custom parameters."""
        cewlio = CeWLio(
            min_word_length=5,
            max_word_length=10,
            lowercase=True,
            with_numbers=True,
            convert_umlauts=True,
            show_count=True
        )
        self.assertEqual(cewlio.min_word_length, 5)
        self.assertEqual(cewlio.max_word_length, 10)
        self.assertTrue(cewlio.lowercase)
        self.assertTrue(cewlio.with_numbers)
        self.assertTrue(cewlio.convert_umlauts)
        self.assertTrue(cewlio.show_count)

    def test_clean_html(self):
        """Test HTML cleaning functionality."""
        html = "<p>Test content</p><!-- comment --><script>var x = 1;</script>"
        cleaned = self.cewlio.clean_html(html)
        self.assertNotIn("<p>", cleaned)
        self.assertNotIn("<!-- comment -->", cleaned)
        self.assertNotIn("<script>", cleaned)
        self.assertIn("Test content", cleaned)

    def test_extract_emails(self):
        """Test email extraction functionality."""
        text = "Contact us at test@example.com or user@domain.org"
        emails = self.cewlio.extract_emails(text)
        self.assertEqual(len(emails), 2)
        self.assertIn("test@example.com", emails)
        self.assertIn("user@domain.org", emails)
        self.assertIn("test@example.com", self.cewlio.emails)
        self.assertIn("user@domain.org", self.cewlio.emails)

    def test_extract_emails_mailto(self):
        """Test email extraction from mailto links."""
        text = '<a href="mailto:contact@example.com">Contact</a>'
        emails = self.cewlio.extract_emails(text)
        self.assertIn("contact@example.com", emails)

    def test_extract_metadata(self):
        """Test metadata extraction from HTML."""
        html = '''
        <meta name="description" content="Test description">
        <meta name="keywords" content="test, keywords">
        <meta name="author" content="Test Author">
        '''
        self.cewlio.extract_metadata(html)
        self.assertIn("Test description", self.cewlio.metadata)
        self.assertIn("test, keywords", self.cewlio.metadata)
        self.assertIn("Test Author", self.cewlio.metadata)

    def test_process_words_basic(self):
        """Test basic word processing."""
        text = "This is a test with some words"
        self.cewlio.process_words(text)
        self.assertIn("This", self.cewlio.words)
        self.assertIn("test", self.cewlio.words)
        self.assertIn("words", self.cewlio.words)
        self.assertNotIn("is", self.cewlio.words)  # Too short (length < 3)

    def test_process_words_lowercase(self):
        """Test word processing with lowercase conversion."""
        cewlio = CeWLio(lowercase=True)
        text = "This Is A Test"
        cewlio.process_words(text)
        self.assertIn("this", cewlio.words)
        self.assertIn("test", cewlio.words)
        self.assertNotIn("This", cewlio.words)

    def test_process_words_with_numbers(self):
        """Test word processing with numbers allowed."""
        cewlio = CeWLio(with_numbers=True)
        text = "Test123 word456 normal"
        cewlio.process_words(text)
        self.assertIn("Test123", cewlio.words)
        self.assertIn("word456", cewlio.words)
        self.assertIn("normal", cewlio.words)

    def test_process_words_convert_umlauts(self):
        """Test word processing with umlaut conversion."""
        cewlio = CeWLio(convert_umlauts=True)
        text = "München Köln über"
        cewlio.process_words(text)
        self.assertIn("Muenchen", cewlio.words)
        self.assertIn("Koeln", cewlio.words)
        self.assertIn("ueber", cewlio.words)

    def test_process_words_length_filtering(self):
        """Test word processing with length filtering."""
        cewlio = CeWLio(min_word_length=4, max_word_length=6)
        text = "short longword verylongword"
        cewlio.process_words(text)
        self.assertIn("short", cewlio.words)  # 5 chars, within range
        self.assertNotIn("longword", cewlio.words)  # 8 chars, too long
        self.assertNotIn("verylongword", cewlio.words)  # 12 chars, too long

    def test_process_words_groups(self):
        """Test word group generation."""
        text = "This is a test sentence"
        self.cewlio.process_words(text, group_size=2)
        self.assertIn("This is", self.cewlio.word_groups)
        self.assertIn("is a", self.cewlio.word_groups)
        self.assertIn("a test", self.cewlio.word_groups)
        self.assertIn("test sentence", self.cewlio.word_groups)

    def test_process_html_complete(self):
        """Test complete HTML processing."""
        self.cewlio.process_html(self.sample_html)
        
        # Check words
        self.assertIn("Welcome", self.cewlio.words)
        self.assertIn("sample", self.cewlio.words)
        self.assertIn("paragraph", self.cewlio.words)
        
        # Check emails
        self.assertIn("test@example.com", self.cewlio.emails)
        self.assertIn("user@domain.org", self.cewlio.emails)
        
        # Check metadata
        self.assertIn("Test website with sample content", self.cewlio.metadata)
        self.assertIn("test, sample, website, content", self.cewlio.metadata)
        self.assertIn("Test Author", self.cewlio.metadata)

    def test_save_results_words_only(self):
        """Test saving results with words only."""
        self.cewlio.words.update(["test", "word", "sample"])
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            self.cewlio.save_results(output_file=f)
            f.seek(0)
            content = f.read()
        
        os.unlink(f.name)
        self.assertIn("test", content)
        self.assertIn("word", content)
        self.assertIn("sample", content)

    def test_save_results_with_counts(self):
        """Test saving results with word counts."""
        cewlio = CeWLio(show_count=True)
        cewlio.words.update(["test", "test", "word"])  # test appears twice
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            cewlio.save_results(output_file=f)
            f.seek(0)
            content = f.read()
        
        os.unlink(f.name)
        self.assertIn("test, 2", content)
        self.assertIn("word, 1", content)

    def test_save_results_emails(self):
        """Test saving email results."""
        self.cewlio.emails.add("test@example.com")
        self.cewlio.emails.add("user@domain.org")
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            self.cewlio.save_results(email_file=f)
            f.seek(0)
            content = f.read()
        
        os.unlink(f.name)
        self.assertIn("test@example.com", content)
        self.assertIn("user@domain.org", content)

    def test_save_results_metadata(self):
        """Test saving metadata results."""
        self.cewlio.metadata.add("Test description")
        self.cewlio.metadata.add("Test keywords")
        
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as f:
            self.cewlio.save_results(metadata_file=f)
            f.seek(0)
            content = f.read()
        
        os.unlink(f.name)
        self.assertIn("Test description", content)
        self.assertIn("Test keywords", content)

    def test_save_results_to_stdout(self):
        """Test saving results to stdout."""
        self.cewlio.words.update(["test", "word"])
        
        # Capture stdout
        captured_output = StringIO()
        sys.stdout = captured_output
        
        try:
            self.cewlio.save_results()
            output = captured_output.getvalue()
            self.assertIn("test", output)
            self.assertIn("word", output)
        finally:
            sys.stdout = sys.__stdout__


class TestExtractHTML(unittest.TestCase):
    """Test cases for the extract_html module."""
    
    @patch('cewlio.extractors.async_playwright')
    def test_extract_html_success(self, mock_playwright):
        """Test successful HTML extraction."""
        async def _test():
            # Mock the playwright context
            mock_context = AsyncMock()
            mock_browser = AsyncMock()
            mock_page = AsyncMock()
            
            mock_playwright.return_value.__aenter__.return_value = mock_context
            mock_context.chromium.launch.return_value = mock_browser
            mock_browser.new_page.return_value = mock_page
            mock_page.content.return_value = "<html><body>Test content</body></html>"
            
            result = await extract_html("https://example.com")
            
            self.assertEqual(result, "<html><body>Test content</body></html>")
            mock_page.goto.assert_called_once()
            mock_browser.close.assert_called_once()
        
        run_async_test(_test)

    @patch('cewlio.extractors.async_playwright')
    def test_extract_html_with_wait_time(self, mock_playwright):
        """Test HTML extraction with wait time."""
        async def _test():
            mock_context = AsyncMock()
            mock_browser = AsyncMock()
            mock_page = AsyncMock()
            
            mock_playwright.return_value.__aenter__.return_value = mock_context
            mock_context.chromium.launch.return_value = mock_browser
            mock_browser.new_page.return_value = mock_page
            mock_page.content.return_value = "<html><body>Test content</body></html>"
            
            result = await extract_html("https://example.com", wait_time=2)
            
            self.assertEqual(result, "<html><body>Test content</body></html>")
            # Check that sleep was called (wait_time > 0)
            # Note: We can't easily test asyncio.sleep in this context
        
        run_async_test(_test)

    @patch('cewlio.extractors.async_playwright')
    def test_extract_html_failure(self, mock_playwright):
        """Test HTML extraction failure."""
        async def _test():
            mock_context = AsyncMock()
            mock_browser = AsyncMock()
            mock_page = AsyncMock()
            
            mock_playwright.return_value.__aenter__.return_value = mock_context
            mock_context.chromium.launch.return_value = mock_browser
            mock_browser.new_page.return_value = mock_page
            mock_page.goto.side_effect = Exception("Network error")
            
            result = await extract_html("https://example.com")
            
            self.assertIsNone(result)
            mock_browser.close.assert_called_once()
        
        run_async_test(_test)


class TestProcessURLWithCeWLio(unittest.TestCase):
    """Test cases for the process_url_with_cewlio function."""
    
    @patch('cewlio.core.extract_html')
    def test_process_url_success(self, mock_extract_html):
        """Test successful URL processing."""
        async def _test():
            mock_extract_html.return_value = """
            <html>
            <head><meta name="description" content="Test description"></head>
            <body>Test content with words</body>
            </html>
            """
            
            cewlio = CeWLio()
            result = await process_url_with_cewlio("https://example.com", cewlio)
            
            self.assertTrue(result)
            self.assertIn("Test", cewlio.words)
            self.assertIn("content", cewlio.words)
            self.assertIn("words", cewlio.words)
            self.assertIn("Test description", cewlio.metadata)
        
        run_async_test(_test)

    @patch('cewlio.core.extract_html')
    def test_process_url_failure(self, mock_extract_html):
        """Test URL processing failure."""
        async def _test():
            mock_extract_html.return_value = None
            
            cewlio = CeWLio()
            result = await process_url_with_cewlio("https://example.com", cewlio)
            
            self.assertFalse(result)
        
        run_async_test(_test)


class TestIntegration(unittest.TestCase):
    """Integration tests for the complete workflow."""
    
    def test_complete_workflow_with_sample_data(self):
        """Test complete workflow with sample HTML data."""
        sample_html = """
        <!DOCTYPE html>
        <html>
        <head>
            <meta name="description" content="Sample website for testing">
            <meta name="keywords" content="test, integration, workflow">
            <meta name="author" content="Test User">
        </head>
        <body>
            <h1>Integration Test Page</h1>
            <p>This page contains various test content including:</p>
            <ul>
                <li>Sample words for extraction</li>
                <li>Contact information: <a href="mailto:contact@test.com">contact@test.com</a></li>
                <li>Another email: user@example.org</li>
            </ul>
            <div title="Additional content" alt="Alternative text">
                More content with different words and phrases.
            </div>
            <!-- Hidden comment -->
            <script>var data = "javascript content";</script>
        </body>
        </html>
        """
        
        # Test with default settings
        cewlio = CeWLio()
        cewlio.process_html(sample_html)
        
        # Check words
        expected_words = ["Integration", "Test", "Page", "contains", "various", "content", "including"]
        for word in expected_words:
            self.assertIn(word, cewlio.words)
        
        # Check emails
        self.assertIn("contact@test.com", cewlio.emails)
        self.assertIn("user@example.org", cewlio.emails)
        
        # Check metadata
        self.assertIn("Sample website for testing", cewlio.metadata)
        self.assertIn("test, integration, workflow", cewlio.metadata)
        self.assertIn("Test User", cewlio.metadata)

    def test_word_groups_integration(self):
        """Test word groups functionality in integration."""
        sample_html = "<body>This is a test sentence with multiple words</body>"
        
        cewlio = CeWLio()
        cewlio.process_html(sample_html, group_size=3)
        
        expected_groups = ["This is a", "is a test", "a test sentence", "test sentence with"]
        for group in expected_groups:
            self.assertIn(group, cewlio.word_groups)

    def test_file_output_integration(self):
        """Test file output functionality."""
        sample_html = "<body>Test content with words</body>"
        
        cewlio = CeWLio()
        cewlio.process_html(sample_html)
        
        # Test word output
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as word_file:
            cewlio.save_results(output_file=word_file)
            word_file.seek(0)
            word_content = word_file.read()
        
        # Test email output
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as email_file:
            cewlio.save_results(email_file=email_file)
            email_file.seek(0)
            email_content = email_file.read()
        
        # Test metadata output
        with tempfile.NamedTemporaryFile(mode='w+', delete=False) as metadata_file:
            cewlio.save_results(metadata_file=metadata_file)
            metadata_file.seek(0)
            metadata_content = metadata_file.read()
        
        # Clean up
        os.unlink(word_file.name)
        os.unlink(email_file.name)
        os.unlink(metadata_file.name)
        
        # Verify content
        self.assertIn("Test", word_content)
        self.assertIn("content", word_content)
        self.assertIn("words", word_content)


class TestEdgeCases(unittest.TestCase):
    """Test edge cases and error conditions."""
    
    def test_empty_html(self):
        """Test processing empty HTML."""
        cewlio = CeWLio()
        cewlio.process_html("")
        self.assertEqual(len(cewlio.words), 0)
        self.assertEqual(len(cewlio.emails), 0)
        self.assertEqual(len(cewlio.metadata), 0) 

    def test_html_with_only_comments(self):
        """Test processing HTML with only comments."""
        html = "<!-- This is a comment --><!-- Another comment -->"
        cewlio = CeWLio()
        cewlio.process_html(html)
        self.assertEqual(len(cewlio.words), 0)

    def test_html_with_only_scripts(self):
        """Test processing HTML with only script tags."""
        html = "<script>var x = 1; var y = 2;</script>"
        cewlio = CeWLio()
        cewlio.process_html(html)
        self.assertEqual(len(cewlio.words), 0)

    def test_very_long_words(self):
        """Test processing with very long words."""
        html = "<body>This is a verylongwordthatiswaytoolong and normal</body>"
        cewlio = CeWLio(max_word_length=10)
        cewlio.process_html(html)
        self.assertIn("normal", cewlio.words)
        self.assertNotIn("verylongwordthatiswaytoolong", cewlio.words)

    def test_words_with_special_characters(self):
        """Test processing words with special characters."""
        html = "<body>Test-word test_word test@word test#word</body>"
        cewlio = CeWLio()
        cewlio.process_html(html)
        # Should only extract "Test" and "test" (before special chars)
        self.assertIn("Test", cewlio.words)
        self.assertIn("test", cewlio.words)

    def test_umlaut_conversion_edge_cases(self):
        """Test umlaut conversion edge cases."""
        html = "<body>München Köln über ß</body>"
        # Use min_word_length=1 to handle any umlaut conversions that might result in single letters
        cewlio = CeWLio(convert_umlauts=True, min_word_length=1)
        cewlio.process_html(html)
        self.assertIn("Muenchen", cewlio.words)
        self.assertIn("Koeln", cewlio.words)
        self.assertIn("ueber", cewlio.words)
        self.assertIn("ss", cewlio.words)  # ß converts to ss

    def test_email_edge_cases(self):
        """Test email extraction edge cases."""
        html = """
        <body>
            <a href="mailto:test@example.com">Email</a>
            <a href="mailto:user@domain.org?subject=test">Email with params</a>
            <p>Invalid email: test@</p>
            <p>Another invalid: @domain.com</p>
        </body>
        """
        cewlio = CeWLio()
        cewlio.process_html(html)
        self.assertIn("test@example.com", cewlio.emails)
        self.assertIn("user@domain.org", cewlio.emails)
        self.assertNotIn("test@", cewlio.emails)
        self.assertNotIn("@domain.com", cewlio.emails)


def run_async_test(test_func):
    """Helper function to run async tests."""
    return asyncio.run(test_func())


if __name__ == '__main__':
    # Create test suite
    test_suite = unittest.TestSuite()
    
    # Add test classes
    test_classes = [
        TestCeWLio,
        TestExtractHTML,
        TestProcessURLWithCeWLio,
        TestIntegration,
        TestEdgeCases
    ]
    
    for test_class in test_classes:
        tests = unittest.TestLoader().loadTestsFromTestCase(test_class)
        test_suite.addTests(tests)
    
    # Run tests
    runner = unittest.TextTestRunner(verbosity=2)
    result = runner.run(test_suite)
    
    # Print summary
    print(f"\n{'='*50}")
    print(f"TEST SUMMARY")
    print(f"{'='*50}")
    print(f"Tests run: {result.testsRun}")
    print(f"Failures: {len(result.failures)}")
    print(f"Errors: {len(result.errors)}")
    print(f"Success rate: {((result.testsRun - len(result.failures) - len(result.errors)) / result.testsRun * 100):.1f}%")
    
    if result.failures:
        print(f"\nFAILURES:")
        for test, traceback in result.failures:
            print(f"- {test}: {traceback}")
    
    if result.errors:
        print(f"\nERRORS:")
        for test, traceback in result.errors:
            print(f"- {test}: {traceback}")
    
    # Exit with appropriate code
    sys.exit(len(result.failures) + len(result.errors)) 