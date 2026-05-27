import os
import re
import sys

def validate_folders():
    errors = []
    tactic_folders = []
    # Get all entries and sort them to ensure consistent order
    entries = sorted(os.listdir('.'))
    for entry in entries:
        if os.path.isdir(entry) and not entry.startswith('.') and entry != 'scripts' and entry != '.github' and entry != 'templates' and entry != 'DFIR':
            if not re.match(r'^\d{2}-[\w]+$', entry):
                errors.append(f"Invalid folder name: {entry}. Must match 00-Name format.")
            else:
                tactic_folders.append(entry)
    return tactic_folders, errors

def validate_file_content(filepath):
    errors = []
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()
            lines = content.splitlines()
    except Exception as e:
        return [f"Could not read file: {e}"]

    # Check headers
    required_headers = [
        'Title', 'Description', 'Severity', 'Category', 'MITRE ATT&CK', 'Author'
    ]
    header_found = {h: False for h in required_headers}

    for line in lines[:20]: # Check first 20 lines for headers
        for h in required_headers:
            if line.strip().startswith(f'// {h}:'):
                header_found[h] = True

    for h, found in header_found.items():
        if not found:
            errors.append(f"Missing header: {h}")

    # Check verbatim strings and invalid comments
    for i, line in enumerate(lines):
        # KQL uses // for comments. # is not a comment and often a syntax error if misplaced.
        # Check for # that is not inside a string

        # Strip comments for string validation
        code_line = line.split('//')[0]

        j = 0
        while j < len(code_line):
            if code_line[j] == '#':
                 errors.append(f"Line {i+1}: Found potential invalid comment '#' (KQL uses //)")
                 break

            if code_line[j] == '"':
                # Check if it's preceded by @
                if j == 0 or code_line[j-1] != '@':
                    errors.append(f"Line {i+1}: Found non-verbatim string (missing @ before \")")
                    break

                # It is a verbatim string, skip to end
                j += 1 # move past opening "
                while j < len(code_line):
                    if code_line[j] == '"':
                        if j + 1 < len(code_line) and code_line[j+1] == '"':
                            j += 2 # escaped quote "" in verbatim string
                        else:
                            # end of string
                            break
                    else:
                        j += 1
            j += 1

    return errors

def main():
    tactic_folders, folder_errors = validate_folders()
    all_errors = folder_errors

    for folder in tactic_folders:
        files = sorted(os.listdir(folder))
        for file in files:
            if file.endswith('.kql'):
                if not re.match(r'^T\d{4}-[\w-]+\.kql$', file):
                    all_errors.append(f"Invalid file name: {folder}/{file}. Must match Txxxx-Name.kql format.")

                file_path = os.path.join(folder, file)
                file_errors = validate_file_content(file_path)
                for err in file_errors:
                    all_errors.append(f"{file_path}: {err}")
            elif not file.startswith('.'):
                 all_errors.append(f"Unexpected file type in tactic folder: {folder}/{file}")

    if all_errors:
        print(f"Validation failed with {len(all_errors)} errors:")
        for err in all_errors:
            print(f"  - ERROR: {err}")
        sys.exit(1)
    else:
        print("Validation successful!")
        sys.exit(0)

if __name__ == "__main__":
    main()
