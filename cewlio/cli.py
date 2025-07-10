#!/usr/bin/env python3
"""
Command-line interface for CeWLio.
"""

import argparse
import asyncio
import sys
import warnings
from pathlib import Path
from typing import Optional
from importlib.metadata import version, PackageNotFoundError

from .core import CeWLio, process_url_with_cewlio


def validate_positive_int(value: str, allow_zero: bool = False) -> int:
    """Validate that the value is a positive integer (or non-negative if allow_zero=True)."""
    try:
        # Strip quotes if present
        cleaned_value = value.strip('"\'')
        int_value = int(cleaned_value)
        if allow_zero:
            if int_value < 0:
                raise argparse.ArgumentTypeError(f"Value must be a non-negative integer, got {int_value}")
        else:
            if int_value <= 0:
                raise argparse.ArgumentTypeError(f"Value must be a positive integer, got {int_value}")
        return int_value
    except ValueError:
        raise argparse.ArgumentTypeError(f"Value must be a valid integer, got '{value}'")


def validate_non_negative_int(value: str) -> int:
    """Validate that the value is a non-negative integer (wrapper for validate_positive_int)."""
    return validate_positive_int(value, allow_zero=True)

def get_version() -> str:
    """Get version from package metadata."""
    try:
        return version("cewlio")
    except PackageNotFoundError:
        # Fallback: read directly from pyproject.toml
        try:
            import tomllib
            pyproject_path = Path(__file__).parent.parent.parent / "pyproject.toml"
            with open(pyproject_path, "rb") as f:
                data = tomllib.load(f)
                return data["project"]["version"]
        except (FileNotFoundError, KeyError, tomllib.TOMLDecodeError):
            return "unknown"


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="CeWLio - Custom word list generator for web content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cewlio https://example.com
  cewlio https://example.com --output words.txt
  cewlio https://example.com -w 5 -e -a
  cewlio https://example.com -m 4 --max-length 12
  cewlio https://example.com --groups 3 -c
        """
    )
    
    # Version argument
    parser.add_argument(
        "--version",
        action="version",
        version=f"CeWLio {get_version()}"
    )
    
    # URL argument
    parser.add_argument(
        "url",
        help="URL to extract words from"
    )
    
    # Output options
    parser.add_argument(
        "-o", "--output",
        help="Output file for words (default: stdout)"
    )
    parser.add_argument(
        "-e", "--email",
        action="store_true",
        help="Include email addresses"
    )
    parser.add_argument(
        "--email_file",
        help="Output file for email addresses"
    )
    parser.add_argument(
        "-a", "--meta",
        action="store_true",
        help="Include meta data"
    )
    parser.add_argument(
        "--meta_file",
        help="Output file for meta data"
    )
    
    # Word processing options
    parser.add_argument(
        "-m", "--min_word_length",
        type=validate_positive_int,
        default=3,
        help="Minimum word length (positive integer), default 3"
    )
    parser.add_argument(
        "--max-length",
        type=validate_positive_int,
        help="Maximum word length (positive integer, default: no limit)"
    )
    parser.add_argument(
        "--lowercase",
        action="store_true",
        help="Convert words to lowercase"
    )
    parser.add_argument(
        "--with-numbers",
        action="store_true",
        help="Include words with numbers"
    )
    parser.add_argument(
        "--convert-umlauts",
        action="store_true",
        help="Convert umlaut characters (ä→ae, ö→oe, ü→ue, ß→ss)"
    )
    parser.add_argument(
        "-c", "--count",
        action="store_true",
        help="Show the count for each word found"
    )
    
    # Word groups
    parser.add_argument(
        "--groups",
        type=validate_positive_int,
        metavar="SIZE",
        help="Generate word groups of specified size (positive integer)"
    )
    
    # Browser options
    parser.add_argument(
        "-w", "--wait",
        type=validate_non_negative_int,
        default=0,
        help="Wait time in seconds for JavaScript execution (non-negative integer, default: 0)"
    )
    parser.add_argument(
        "--visible",
        action="store_true",
        help="Show browser window (default: headless)"
    )
    parser.add_argument(
        "--timeout",
        type=validate_positive_int,
        default=30000,
        help="Browser timeout in milliseconds (positive integer, default: 30000)"
    )

    
    # Debug/verbose flag
    parser.add_argument(
        "--debug",
        action="store_true",
        help="Show debug/summary output"
    )
    
    return parser


def main() -> None:
    """Main CLI entry point."""
    
    # Check for Playwright availability early
    try:
        import playwright
    except ImportError:
        print("❌ Playwright is not installed.", file=sys.stderr)
        print("", file=sys.stderr)
        print("CeWLio requires Playwright for browser automation.", file=sys.stderr)
        print("", file=sys.stderr)
        print("To install:", file=sys.stderr)
        print("1. pip install playwright", file=sys.stderr)
        print("2. playwright install chromium-headless-shell", file=sys.stderr)
        print("", file=sys.stderr)
        print("For more information, see: https://playwright.dev/python/docs/installation", file=sys.stderr)
        sys.exit(1)
    
    # Check if browser is installed (optional check)
    try:
        from playwright.async_api import async_playwright
        import asyncio
        
        async def check_browser():
            async with async_playwright() as p:
                try:
                    browser = await p.chromium.launch(headless=True)
                    await browser.close()
                    return True
                except KeyboardInterrupt:
                    return False
                except Exception:
                    return False
        
        # Run a quick browser check
        if not asyncio.run(check_browser()):
            print("⚠️  Warning: Chromium browser may not be properly installed.", file=sys.stderr)
            print("If you encounter browser errors, run: playwright install chromium-headless-shell", file=sys.stderr)
            print("", file=sys.stderr)
    except KeyboardInterrupt:
        print("\n⏹️  Browser check cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception:
        # If browser check fails, continue anyway - the actual error will be caught later
        pass
    
    parser = create_parser()
    args = parser.parse_args()
    
    # Validate that max_length is greater than min_word_length if both are specified
    if args.max_length is not None and args.max_length <= args.min_word_length:
        print(f"Error: Maximum word length ({args.max_length}) must be greater than minimum word length ({args.min_word_length})", file=sys.stderr)
        sys.exit(1)
    
    # Create CeWLio instance
    cewlio = CeWLio(
        min_word_length=args.min_word_length,
        max_word_length=args.max_length,
        lowercase=args.lowercase,
        with_numbers=args.with_numbers,
        convert_umlauts=args.convert_umlauts,
        show_count=args.count
    )
    
    # Handle output files
    output_file = None
    email_file = None
    metadata_file = None
    
    if args.output:
        try:
            output_file = open(args.output, 'w', encoding='utf-8')
        except IOError as e:
            print(f"Error opening output file: {e}", file=sys.stderr)
            sys.exit(1)
    
    if args.email_file:
        try:
            email_file = open(args.email_file, 'w', encoding='utf-8')
        except IOError as e:
            print(f"Error opening email file: {e}", file=sys.stderr)
            sys.exit(1)
    
    if args.meta_file:
        try:
            metadata_file = open(args.meta_file, 'w', encoding='utf-8')
        except IOError as e:
            print(f"Error opening metadata file: {e}", file=sys.stderr)
            sys.exit(1)
    
    try:
        # Process the URL with proper exception handling
        async def run_with_exception_handling():
            try:
                return await process_url_with_cewlio(
                    url=args.url,
                    cewlio_instance=cewlio,
                    group_size=args.groups,
                    output_file=output_file,
                    email_file=email_file,
                    metadata_file=metadata_file,
                    show_emails=args.email,
                    show_metadata=args.meta,
                    wait_time=args.wait,
                    headless=not args.visible,
                    timeout=args.timeout,
                    debug=args.debug
                )
            except KeyboardInterrupt:
                print("\n⏹️  Operation cancelled by user", file=sys.stderr)
                return False
            except Exception as e:
                # Let the outer exception handler deal with it
                raise
        
        success = asyncio.run(run_with_exception_handling())
        
        if not success:
            sys.exit(1)
        
        # Print summary only if debug
        if args.debug:
            print(f"\nProcessing complete!", file=sys.stderr)
            print(f"Words found: {len(cewlio.words)}", file=sys.stderr)
            if args.groups:
                print(f"Word groups found: {len(cewlio.word_groups)}", file=sys.stderr)
            if args.email or args.email_file or cewlio.emails:
                print(f"Email addresses found: {len(cewlio.emails)}", file=sys.stderr)
            if args.meta or args.meta_file or cewlio.metadata:
                print(f"Metadata items found: {len(cewlio.metadata)}", file=sys.stderr)
    
    except KeyboardInterrupt:
        print("\n⏹️  Operation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except ImportError as e:
        if "playwright" in str(e).lower():
            print("❌ Playwright is not installed or not available.", file=sys.stderr)
            print("", file=sys.stderr)
            print("To fix this issue:", file=sys.stderr)
            print("1. Install Playwright: pip install playwright", file=sys.stderr)
            print("2. Install the browser: playwright install chromium-headless-shell", file=sys.stderr)
            print("", file=sys.stderr)
            print("For more information, see: https://playwright.dev/python/docs/installation", file=sys.stderr)
        else:
            print(f"❌ Import error: {e}", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        error_msg = str(e).lower()
        if "browser" in error_msg and ("not found" in error_msg or "not installed" in error_msg):
            print("❌ Browser not found. Please install the required browser:", file=sys.stderr)
            print("", file=sys.stderr)
            print("playwright install chromium-headless-shell", file=sys.stderr)
        elif "timeout" in error_msg:
            print("❌ Browser timeout. The page took too long to load.", file=sys.stderr)
            print("", file=sys.stderr)
            print("Try increasing the timeout with --timeout or wait time with -w", file=sys.stderr)
            print("Example: cewlio https://example.com --timeout 60000 -w 10", file=sys.stderr)
        elif "network" in error_msg or "connection" in error_msg or "err_aborted" in error_msg:
            print("❌ Network error. Unable to connect to the website.", file=sys.stderr)
            print("", file=sys.stderr)
            print("Please check:", file=sys.stderr)
            print("- Your internet connection", file=sys.stderr)
            print("- The URL is correct and accessible", file=sys.stderr)
            print("- The website is not blocking automated access", file=sys.stderr)
        elif "playwright" in error_msg:
            # Handle Playwright-specific errors without showing traceback
            print("❌ Browser error occurred during page processing.", file=sys.stderr)
            print("", file=sys.stderr)
            print("This could be due to:", file=sys.stderr)
            print("- Website blocking automated access", file=sys.stderr)
            print("- Network connectivity issues", file=sys.stderr)
            print("- Browser timeout (try increasing --timeout)", file=sys.stderr)
        else:
            print(f"❌ Error: {e}", file=sys.stderr)
        sys.exit(1)
    finally:
        # Close files
        if output_file:
            output_file.close()
        if email_file:
            email_file.close()
        if metadata_file:
            metadata_file.close()


if __name__ == "__main__":
    main() 