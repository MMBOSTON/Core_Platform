"""
Generate a textual representation of the project structure and saving it to a text file.
Automatically use the current working directory as the project root when no specific path is provided. 
"""

import os
from datetime import datetime

def generate_project_structure(path, indent=0, max_depth=4):
    structure = ""
    if not os.path.exists(path):
        return structure
    
    if os.path.isfile(path):
        structure += '│   ' * indent + '├── ' + os.path.basename(path) + '\n'
    elif os.path.isdir(path):
        if os.path.basename(path) in ['.git', '__pycache__', '.venv'] or \
           '@' in os.path.basename(path) or \
           'node_modules' in path or 'build' in path:  # Ignore directories at any level
            return structure
        
        structure += '│   ' * indent + '├── ' + os.path.basename(path) + '/\n'
        if indent < max_depth:
            for child in sorted(os.listdir(path)):
                if child.startswith('.'):
                    continue
                
                structure += generate_project_structure(os.path.join(path, child), indent+1, max_depth=max_depth)
    
    return structure

def save_to_file(project_structure, filename):
    with open(filename, 'w', encoding='utf-8') as f:
        f.write(project_structure)

if __name__ == "__main__":
    project_path = os.getcwd()
    project_structure = generate_project_structure(project_path)
    
    datestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    filename = f"project_structure_tree_{datestamp}.txt"
    save_to_file(project_structure, filename)
    
    print(f"Project structure saved to {filename}")