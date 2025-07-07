#!/usr/bin/env python3
"""
HTML Extractor - Extract HTML from DOM after JavaScript execution
Uses Playwright to load a webpage, wait for JS to complete, then extract the HTML.
"""

import asyncio
import argparse
import sys
from pathlib import Path
from playwright.async_api import async_playwright


async def extract_html(url, output_file=None, wait_time=0, headless=True, timeout=30000, debug=False):
    """
    Extract HTML from a webpage after JavaScript execution.
    
    Args:
        url (str): The URL to extract HTML from
        output_file (str, optional): File path to save the HTML
        wait_time (int): Additional time to wait after page load (seconds)
        headless (bool): Whether to run browser in headless mode
        timeout (int): Timeout in milliseconds for page load
    """
    async with async_playwright() as p:
        # Launch browser
        browser = await p.chromium.launch(headless=headless)
        page = await browser.new_page()
        
        try:
            if debug:
                print(f"Loading page: {url}")
            
            # Try different wait strategies in order of preference
            wait_strategies = [
                'domcontentloaded',  # Wait for DOM to be ready
                'load',              # Wait for page load event
                'networkidle'        # Wait for network to be idle (most strict)
            ]
            
            html_content = None
            last_error = None
            
            for strategy in wait_strategies:
                try:
                    if debug:
                        print(f"Trying wait strategy: {strategy}")
                    await page.goto(url, wait_until=strategy, timeout=timeout)
                    
                    # Additional wait time if specified
                    if wait_time > 0:
                        if debug:
                            print(f"Waiting additional {wait_time} seconds...")
                        await asyncio.sleep(wait_time)
                    
                    # Extract the HTML content
                    html_content = await page.content()
                    if debug:
                        print(f"Successfully extracted HTML using {strategy} strategy")
                    break
                    
                except Exception as e:
                    last_error = e
                    if debug:
                        print(f"Strategy {strategy} failed: {e}")
                    continue
            
            if html_content is None:
                if debug:
                    print(f"All wait strategies failed. Last error: {last_error}")
                return None
            
            if output_file:
                # Save to file
                with open(output_file, 'w', encoding='utf-8') as f:
                    f.write(html_content)
                if debug:
                    print(f"HTML saved to: {output_file}")
            else:
                # Print to console only if debug is enabled
                if debug:
                    print("\n" + "="*50)
                    print("EXTRACTED HTML:")
                    print("="*50)
                    print(html_content)
            
            return html_content
            
        except Exception as e:
            if debug:
                print(f"Error: {e}")
            return None
        finally:
            await browser.close()


def main():
    parser = argparse.ArgumentParser(
        description="Extract HTML from a webpage after JavaScript execution"
    )
    parser.add_argument("url", help="URL to extract HTML from")
    parser.add_argument(
        "-o", "--output", 
        help="Output file path (if not specified, prints to console)"
    )
    parser.add_argument(
        "-w", "--wait", 
        type=int, 
        default=0,
        help="Additional wait time in seconds after page load"
    )
    parser.add_argument(
        "--visible", 
        action="store_true",
        help="Run browser in visible mode (not headless)"
    )
    parser.add_argument(
        "-t", "--timeout",
        type=int,
        default=30000,
        help="Timeout in milliseconds for page load (default: 30000)"
    )
    
    args = parser.parse_args()
    
    # Run the extraction
    html = asyncio.run(extract_html(
        url=args.url,
        output_file=args.output,
        wait_time=args.wait,
        headless=not args.visible,
        timeout=args.timeout
    ))
    
    if html is None:
        sys.exit(1)


if __name__ == "__main__":
    main() 