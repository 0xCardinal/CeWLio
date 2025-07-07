"""
CeWLio - Custom word list generator for web content.

A Python tool for extracting words, emails, and metadata from HTML content,
similar to the original CeWL tool but with enhanced features.
"""

from .core import CeWLio, process_url_with_cewlio
from .extractors import extract_html

try:
    from importlib.metadata import version
    __version__ = version("cewlio")
except ImportError:
    __version__ = "1.1.1"

__author__ = "Kumar Ashwin"
__email__ = "kumar.ashwin@example.com"

__all__ = [
    "CeWLio",
    "process_url_with_cewlio", 
    "extract_html",
    "__version__",
    "__author__",
    "__email__"
] 