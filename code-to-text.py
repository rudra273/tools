import os

# List of directories and file patterns to exclude
EXCLUDE_DIRS = {'.git', '.cache', 'node_modules', '__pycache__', '.idea', '.vscode', '.npm'}
EXCLUDE_FILES = {'.lock', '.DS_Store', '.hcl'}

def print_folder_tree_to_file(folder_path, output_file, indent=0):
    """Print the folder structure as a tree to the output file, excluding certain dirs and files."""
    try:
        entries = os.listdir(folder_path)
        
        for entry in entries:
            full_path = os.path.join(folder_path, entry)
            
            # Skip excluded directories and files
            if any(exclude in full_path for exclude in EXCLUDE_DIRS):
                continue
            if any(full_path.endswith(exclude) for exclude in EXCLUDE_FILES):
                continue
            
            if os.path.isdir(full_path):
                output_file.write('  ' * indent + f"DIR: {entry}\n")
                print_folder_tree_to_file(full_path, output_file, indent + 1)
            else:
                output_file.write('  ' * indent + f"FILE: {entry}\n")
    except Exception as e:
        print(f"Error while printing folder structure: {e}")

def copy_code_to_text(folder_path, output_file):
    """Copy contents of all files in the folder and subfolders into a text file, excluding certain files and dirs."""
    try:
        with open(output_file, 'w', encoding='utf-8') as output:
            # First write the folder structure
            output.write("Folder Structure:\n")
            print_folder_tree_to_file(folder_path, output)
            
            # Now write the contents of all files
            output.write("\n\n--- Files Code ---\n")
            
            for root, dirs, files in os.walk(folder_path):
                # Modify dirs in-place to skip certain folders like .git, .cache, etc.
                dirs[:] = [d for d in dirs if d not in EXCLUDE_DIRS]
                
                for file in files:
                    file_path = os.path.join(root, file)
                    
                    # Skip excluded files
                    if any(file.endswith(exclude) for exclude in EXCLUDE_FILES):
                        continue
                    
                    try:
                        with open(file_path, 'r', encoding='utf-8') as f:
                            output.write(f"\n\n--- {file_path} ---\n")
                            output.write(f.read())  # Copy the content of the file
                    except Exception as e:
                        print(f"Could not read file {file_path}: {e}")
    except Exception as e:
        print(f"Error while writing to the output file: {e}")

def main():
    # Ask the user for the absolute folder path
    folder_path = input("Please enter the absolute path of the folder: ")
    
    if not os.path.isdir(folder_path):
        print(f"The provided path '{folder_path}' is not a valid directory.")
        return
    
    # Ask the user for the name of the output text file
    output_file_name = input("Please enter the name of the output text file (e.g., output.txt): ")
    output_file = os.path.join(folder_path, output_file_name)
    
    print(f"\nCopying folder structure and files' code from '{folder_path}' to '{output_file}'...")
    copy_code_to_text(folder_path, output_file)
    print(f"\nFinished copying folder structure and all files' code to '{output_file}'.")

if __name__ == "__main__":
    main()
