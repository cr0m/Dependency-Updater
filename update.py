#!/usr/bin/env python3

import os
import re
import sys
import requests
from urllib.parse import urlparse

# ANSI escape codes for colors
RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
CYAN = '\033[36m'
RESET = '\033[0m'

def download_file(url, local_folder):
    """Download a file from a URL and save it to a specified local folder."""
    parsed_url = urlparse(url)
    filename = os.path.basename(parsed_url.path)
    local_path = os.path.join(local_folder, filename)

    # Ensure the folder exists
    os.makedirs(local_folder, exist_ok=True)

    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
        with open(local_path, 'wb') as file:
            file.write(response.content)
        print(f"{GREEN}Downloaded: {CYAN}{url} {RESET}-> {YELLOW}{local_path}")
    except requests.exceptions.RequestException as e:
        print(f"{RED}Failed to download {url}: {e}{RESET}")
        return None

    return filename

def process_file(file_path):
    """Process a PHP file, find and replace external CSS/JS dependencies."""
    if not os.path.isfile(file_path):
        print(f"{RED}File not found: {file_path}{RESET}")
        return

    # Patterns to match CSS and JS links
    patterns = [
        r'<link.*?href="(http[^"]+\.css)".*?>',
        r'<script.*?src="(http[^"]+\.js)".*?>'
    ]

    local_folders = {
        '.css': 'css',
        '.js': 'js'
    }

    updated_count = 0
    downloaded_files = []

    with open(file_path, 'r') as file:
        content = file.read()

    for pattern in patterns:
        matches = re.findall(pattern, content)
        for match in matches:
            ext = os.path.splitext(match)[1]
            local_folder = local_folders.get(ext, '')
            if not local_folder:
                continue

            filename = download_file(match, local_folder)
            if filename:
                local_path = f"./{local_folder}/{filename}"
                content = content.replace(match, local_path)
                updated_count += 1
                downloaded_files.append(match)

    # No matches found
    if updated_count == 0:
        print(f"{YELLOW}No external dependencies found in {file_path}.{RESET}")
        return

    # Write updated content back to the file
    with open(file_path, 'w') as file:
        file.write(content)

    print(f"{GREEN}Processed: {CYAN}{file_path}{RESET}")
    print(f"{GREEN}Found and updated {YELLOW}{updated_count} {GREEN}external dependencies.{RESET}")
    print(f"{GREEN}Updated references:{RESET}")
    for original in downloaded_files:
        print(f"  - {CYAN}{original}{RESET}")

def process_directory():
    """Process all PHP files in the current directory."""
    php_files = [f for f in os.listdir('.') if f.endswith('.php')]

    if not php_files:
        print(f"{RED}No PHP files found in the current directory.{RESET}")
        return

    print(f"{YELLOW}Found the following PHP files:{RESET}")
    for php_file in php_files:
        print(f"  - {CYAN}{php_file}{RESET}")

    proceed = input(f"{YELLOW}Do you want to process all PHP files? (y/n): {RESET}").strip().lower()
    if proceed != 'y':
        print(f"{RED}Operation cancelled.{RESET}")
        return

    for php_file in php_files:
        process_file(php_file)

if __name__ == "__main__":
    if len(sys.argv) == 2:
        file_to_process = sys.argv[1]
        process_file(file_to_process)
    elif len(sys.argv) == 1:
        print(f"{YELLOW}No filename provided.{RESET}")
        process_directory()
    else:
        print(f"{RED}Usage: ./updatecode.py [filename.php]{RESET}")
        sys.exit(1)

