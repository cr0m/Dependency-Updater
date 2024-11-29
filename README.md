# CSS and JS Dependency Updater

![License](https://img.shields.io/badge/license-MIT-blue.svg)

## Table of Contents

- [Overview](#overview)
- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Processing a Single PHP File](#processing-a-single-php-file)
  - [Processing All PHP Files in a Directory](#processing-all-php-files-in-a-directory)
- [Example Output](#example-output)
- [How It Works](#how-it-works)
- [Contributing](#contributing)
- [License](#license)

## Overview

**CSS and JS Dependency Updater** is a Python script designed to streamline the process of managing external CSS and JavaScript dependencies in PHP files. It automates the task of finding external links to CSS and JS files, downloading them locally, and updating the PHP files to reference these local copies instead of external URLs.

## Features

- **Automated Dependency Management**: Identifies and replaces external CSS and JS dependencies with local paths.
- **Batch Processing**: Option to process a single PHP file or all PHP files in the current directory.
- **Download Dependencies**: Automatically downloads the external CSS and JS files to designated local folders.
- **Colored Terminal Output**: Provides color-coded feedback for better readability.
- **Portable**: Utilizes ANSI escape codes for coloring, eliminating the need for external libraries.

## Installation

### Prerequisites

- **Python 3**: Ensure you have Python 3 installed on your system.
- **Requests Library**: The script uses the `requests` module to handle HTTP requests.

### Installing `requests`

If `requests` is not already installed on your system, you can install it using `pip`:

```bash
pip install requests
