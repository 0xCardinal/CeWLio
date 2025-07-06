#!/usr/bin/env python3
"""
Setup script for CeWLio package.
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    readme_path = os.path.join(os.path.dirname(__file__), "README.md")
    if os.path.exists(readme_path):
        with open(readme_path, "r", encoding="utf-8") as f:
            return f.read()
    return "CeWLio - Custom word list generator for web content"

# Read requirements
def read_requirements():
    requirements_path = os.path.join(os.path.dirname(__file__), "requirements.txt")
    if os.path.exists(requirements_path):
        with open(requirements_path, "r", encoding="utf-8") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return [
        "playwright>=1.40.0",
        "beautifulsoup4>=4.12.0",
        "requests>=2.31.0",
    ]

setup(
    name="cewlio",
    version="1.0.0",
    description="Custom word list generator for web content",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    author="Your Name",
    author_email="your.email@example.com",
    url="https://github.com/yourusername/cewlio",
    project_urls={
        "Bug Reports": "https://github.com/yourusername/cewlio/issues",
        "Source": "https://github.com/yourusername/cewlio",
        "Documentation": "https://github.com/yourusername/cewlio#readme",
    },
    packages=find_packages(),
    py_modules=["cewlio"],
    entry_points={
        "console_scripts": [
            "cewlio=cewlio.cli:main",
        ],
    },
    install_requires=read_requirements(),
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-asyncio>=0.21.0",
            "coverage>=7.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    python_requires=">=3.8",
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Topic :: Internet :: WWW/HTTP",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "Topic :: Text Processing :: Linguistic",
        "Topic :: Utilities",
    ],
    keywords="wordlist, web scraping, html parsing, email extraction, metadata",
    license="MIT",
    zip_safe=False,
    include_package_data=True,
) 