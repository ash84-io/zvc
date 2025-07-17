#!/usr/bin/env python3
"""Setup script for zvc package."""

from setuptools import setup, find_packages

if __name__ == "__main__":
    setup(
        name="zvc",
        version="0.1.4",
        packages=find_packages(),
        python_requires=">=3.10",
        classifiers=[
            "Programming Language :: Python :: 3.10",
            "Programming Language :: Python :: 3.11",
            "Programming Language :: Python :: 3.12",
            "Programming Language :: Python :: 3.13",
            "Programming Language :: Python :: Implementation :: CPython",
        ],
    )
