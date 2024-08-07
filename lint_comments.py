import os
import yaml
import re
import sys

def lint_comments(data):
    pattern = r'^#[A-Z].*'
    error_count = 0

    if isinstance(data, dict):
        for key, value in data.items():
            if isinstance(value, str):
                if key.startswith('#'):
                    if not re.match(pattern, key, re.IGNORECASE):
                        print(f'Error: Invalid comment in file: {filepath}')
                        error_count += 1
            elif isinstance(value, (dict, list)):
                error_count += lint_comments(value)
    elif isinstance(data, list):
        for item in data:
            if isinstance(item, (dict, list)):
                error_count += lint_comments(item)

    return error_count

def process_files():
    error_count = 0

    for root, dirs, files in os.walk('.'):
        for file in files:
            if file.endswith('.yaml') or file.endswith('.yml'):
                filepath = os.path.join(root, file)
                with open(filepath, 'r') as f:
                    try:
                        data = yaml.safe_load(f)
                        error_count += lint_comments(data)
                    except yaml.YAMLError as e:
                        print(f'Error: Failed to parse YAML file: {filepath}')
                        error_count += 1

    return error_count

error_count = process_files()

if error_count > 0:
    sys.exit(1)
