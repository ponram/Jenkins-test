from setuptools import setup, find_packages
import os

# Read README file for long description
def read_readme():
    with open("README.md", "r", encoding="utf-8") as fh:
        return fh.read()

# Read requirements from requirements.txt
def read_requirements():
    with open("requirements.txt", "r", encoding="utf-8") as fh:
        return [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="option-pricer",
    version="0.1.0",
    author="Your Name",
    author_email="your.email@example.com",
    description="European option pricing using QuantLib",
    long_description=read_readme(),
    long_description_content_type="text/markdown",
    url="https://github.com/ponram/Jenkins-test",
    project_urls={
        "Bug Tracker": "https://github.com/ponram/Jenkins-test/issues",
    },
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Financial and Insurance Industry",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    python_requires=">=3.8",
    install_requires=read_requirements(),
    extras_require={
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "coverage>=6.0",
        ],
        "dev": [
            "black>=22.0.0",
            "flake8>=5.0.0",
            "isort>=5.0.0",
        ],
    },
    entry_points={
        "console_scripts": [
            "price-option=option_pricer.app:main",
        ],
    },
    include_package_data=True,
    zip_safe=False,
)
