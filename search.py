import os
import re

# Define the pattern for matching the lines
pattern = re.compile(r'^%ignore\s+[a-zA-Z0-9_::]+::[a-zA-Z0-9_]+\(.*&&;\)$')

# Function to search files recursively
def search_files_in_directory(directory):
    matches = []
    
    # Walk through all files in the directory and its subdirectories
    for root, _, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Skip files that are not relevant (e.g., non-text files)
            if not file.endswith((".txt", ".cpp", ".h")):
                continue
            
            # Open and read each file
            try:
                with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                    lines = f.readlines()
                    for line in lines:
                        # Check if the line matches the pattern
                        if pattern.match(line.strip()):
                            matches.append(line.strip())
            except Exception as e:
                print(f"Could not read file {file_path}: {e}")
    
    return matches

# Write the matches to an output file
def write_matches_to_file(matches):
    with open('output.txt', 'w', encoding='utf-8') as output_file:
        for match in matches:
            output_file.write(match + '\n')

# Main function
if __name__ == "__main__":
    directory = '.'  # Current directory
    print("Searching for pattern in files...")
    matches = search_files_in_directory(directory)
    
    if matches:
        write_matches_to_file(matches)
        print(f"Found {len(matches)} matching lines. Results saved in 'output.txt'.")
    else:
        print("No matches found.")
