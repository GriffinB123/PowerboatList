"""Setup configuration for PowerboatList."""

from setuptools import setup, find_packages
from pathlib import Path

# Read version from __version__.py
version = {}
with open("__version__.py") as fp:
    exec(fp.read(), version)

# Read long description from README
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding="utf-8")

setup(
    name="powerboatlist",
    version=version["__version__"],
    author=version["__author__"],
    description=version["__description__"],
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/YOUR_USERNAME/PowerboatList",
    packages=find_packages(),
    py_modules=["search_boats", "__version__"],
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Topic :: Utilities",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    python_requires=">=3.8",
    install_requires=[
        "anthropic>=0.18.0",
        "requests>=2.31.0",
        "python-dotenv>=1.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "pytest-mock>=3.11.1",
            "black>=23.7.0",
            "flake8>=6.1.0",
            "isort>=5.12.0",
            "mypy>=1.5.0",
            "pre-commit>=3.3.3",
        ],
        "colab": [
            "gspread>=5.12.0",
            "oauth2client>=4.1.3",
        ],
    },
    entry_points={
        "console_scripts": [
            "powerboatlist=search_boats:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/YOUR_USERNAME/PowerboatList/issues",
        "Source": "https://github.com/YOUR_USERNAME/PowerboatList",
        "Documentation": "https://github.com/YOUR_USERNAME/PowerboatList/blob/main/README.md",
    },
    keywords="boats powerboat search api anthropic claude brave-search",
    include_package_data=True,
    zip_safe=False,
)
