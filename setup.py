#!/usr/bin/env python3
"""
Setup script for Flucht von der Dinosaurier-Insel
Creates a distributable Python package

Usage:
    python setup.py sdist        # Create source distribution
    python setup.py bdist_wheel  # Create wheel distribution
    pip install dist/dinosaur-island-2.0.0.tar.gz  # Install
"""

from setuptools import setup, find_packages
import os

# Read the long description from README
long_description = ""
if os.path.exists("README.md"):
    with open("README.md", "r", encoding="utf-8") as f:
        long_description = f.read()

# Read requirements
requirements = []
if os.path.exists("requirements.txt"):
    with open("requirements.txt", "r") as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="dinosaur-island",
    version="2.0.0",
    author="Konrad Weber & Stefan Weber",
    author_email="",
    description="Escape from Dinosaur Island - A survival game",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/flucht-von-der-dinosaurier-insel",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Games/Entertainment",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    include_package_data=True,
    package_data={
        "": ["konrad_insel/**/*"],
    },
    entry_points={
        "console_scripts": [
            "dinosaur-island=main:main",
        ],
    },
    zip_safe=False,
)
