#!/usr/bin/env python3
"""
Command-line interface for CeWLio.
"""

import argparse
import asyncio
import sys
from pathlib import Path
from typing import Optional
from importlib.metadata import version, PackageNotFoundError

from .core import CeWLio, process_url_with_cewlio


def get_version() -> str:
    """Get version from package metadata."""
    try:
        return version("cewlio")
    except PackageNotFoundError:
        return "unknown"


def create_parser() -> argparse.ArgumentParser:
    """Create and configure the argument parser."""
    parser = argparse.ArgumentParser(
        description="CeWLio - Custom word list generator for web content",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  cewlio https://example.com
  cewlio https://example.com -o words.txt
  cewlio https://example.com -w 5 --email --metadata
  cewlio https://example.com --min-length 4 --max-length 12
  cewlio https://example.com --groups 3 --count
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
        "--email",
        help="Output file for email addresses"
    )
    parser.add_argument(
        "--metadata",
        help="Output file for metadata"
    )
    
    # Word processing options
    parser.add_argument(
        "--min-length",
        type=int,
        default=3,
        help="Minimum word length (default: 3)"
    )
    parser.add_argument(
        "--max-length",
        type=int,
        help="Maximum word length (default: no limit)"
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
        "--count",
        action="store_true",
        help="Show word counts"
    )
    
    # Word groups
    parser.add_argument(
        "--groups",
        type=int,
        metavar="SIZE",
        help="Generate word groups of specified size"
    )
    
    # Browser options
    parser.add_argument(
        "-w", "--wait",
        type=int,
        default=0,
        help="Wait time in seconds for JavaScript execution (default: 0)"
    )
    parser.add_argument(
        "--visible",
        action="store_true",
        help="Show browser window (default: headless)"
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=30000,
        help="Browser timeout in milliseconds (default: 30000)"
    )
    
    # No words mode
    parser.add_argument(
        "--no-words",
        action="store_true",
        help="Don't extract words, only emails and metadata"
    )
    
    return parser


def main() -> None:
    """Main CLI entry point."""
    parser = create_parser()
    args = parser.parse_args()
    
    # Create CeWLio instance
    cewlio = CeWLio(
        min_word_length=args.min_length,
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
    
    if args.email:
        try:
            email_file = open(args.email, 'w', encoding='utf-8')
        except IOError as e:
            print(f"Error opening email file: {e}", file=sys.stderr)
            sys.exit(1)
    
    if args.metadata:
        try:
            metadata_file = open(args.metadata, 'w', encoding='utf-8')
        except IOError as e:
            print(f"Error opening metadata file: {e}", file=sys.stderr)
            sys.exit(1)
    
    try:
        # Process the URL
        success = asyncio.run(process_url_with_cewlio(
            url=args.url,
            cewlio_instance=cewlio,
            group_size=args.groups,
            output_file=output_file,
            email_file=email_file,
            metadata_file=metadata_file,
            wait_time=args.wait,
            headless=not args.visible,
            timeout=args.timeout
        ))
        
        if not success:
            sys.exit(1)
        
        # Print summary
        print(f"\nProcessing complete!", file=sys.stderr)
        if not args.no_words:
            print(f"Words found: {len(cewlio.words)}", file=sys.stderr)
        if args.groups:
            print(f"Word groups found: {len(cewlio.word_groups)}", file=sys.stderr)
        if args.email or cewlio.emails:
            print(f"Email addresses found: {len(cewlio.emails)}", file=sys.stderr)
        if args.metadata or cewlio.metadata:
            print(f"Metadata items found: {len(cewlio.metadata)}", file=sys.stderr)
    
    except KeyboardInterrupt:
        print("\nOperation cancelled by user", file=sys.stderr)
        sys.exit(1)
    except Exception as e:
        print(f"Error: {e}", file=sys.stderr)
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