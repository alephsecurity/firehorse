#!/usr/bin/env python3
"""
Setup script for firehorse package
"""

from setuptools import setup, find_packages
import os

# Read the README file
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read the LICENSE file
def read_license():
    with open("LICENSE", "r", encoding="utf-8") as fh:
        return fh.read()

setup(
    name="firehorse",
    version="1.0.0",
    author="Roee Hay & Noam Hadad",
    author_email="research@alephsecurity.com",
    description="Research & Exploitation framework for Qualcomm EDL Firehose programmers",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/alephsecurity/firehorse",
    project_urls={
        "Blog": "https://alephsecurity.com/",
        "Research": "https://alephsecurity.com/research/",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: Information Technology",
        "Topic :: Security",
        "Topic :: Software Development :: Embedded Systems",
        "Topic :: System :: Hardware",
        "License :: OSI Approved :: Apache Software License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Operating System :: Microsoft :: Windows",
        "Operating System :: POSIX :: Linux",
    ],
    python_requires=">=3.6",
    install_requires=[
        "pyserial",
        "pyusb",
        "cryptography",
    ],
    extras_require={
        "dev": [
            "pytest",
            "black",
            "flake8",
            "twine",
            "wheel",
            "build",
        ],
    },
    entry_points={
        "console_scripts": [
            "firehorse=firehorse.firehorse:main",
        ],
    },
    include_package_data=True,
    package_data={
        "firehorse": [
            "target/*.xml",
            "target/*.py",
        ],
    },
    keywords="qualcomm edl firehose mobile security research exploitation",
    license="Apache License 2.0",
)
