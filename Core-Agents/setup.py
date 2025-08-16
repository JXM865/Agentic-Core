#!/usr/bin/env python3
"""
Setup script for Core-Agents package
"""

from setuptools import setup, find_packages

setup(
    name="core-agents",
    version="2.0.0",
    description="Core agents for the MTP-2.0 multi-agent trading platform",
    author="MTP Team",
    author_email="team@mtp.com",
    packages=find_packages(),
    python_requires=">=3.8",
    install_requires=[
        "pyyaml>=6.0",
        "asyncio-mqtt>=0.11.0",
    ],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
    ],
)
