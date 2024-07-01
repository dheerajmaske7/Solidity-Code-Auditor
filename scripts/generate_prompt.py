import os
import re
import json
import pandas as pd
from pathlib import Path

def extract_annotations(solidity_code):
    pattern = re.compile(r'@vulnerable_at_lines: (\d+(?:,\d+)*)')
    match = pattern.search(solidity_code)
    if match:
        return list(map(int, match.group(1).split(',')))
    return []

# Remove comments from Solidity code
def remove_comments(solidity_code):
    def replacer(match):
        s = match.group(0)
        if s.startswith('/'):
            return ""
        else:
            return s

    pattern = re.compile(
        r'//.*?$|/\*.*?\*/|\'(?:\\.|[^\\\'])*\'|"(?:\\.|[^\\"])*"',
        re.DOTALL | re.MULTILINE
    )
    
    return re.sub(pattern, replacer, solidity_code)

def remove_comments_and_update_lines(solidity_code, annotations):
    lines = solidity_code.splitlines()
    clean_lines = []
    offset_adjustments = []

    in_block_comment = False

    for i, line in enumerate(lines):
        stripped_line = line.strip()
        if stripped_line.startswith("/*"):
            in_block_comment = True
            if any(annotation <= i + 1 for annotation in annotations):
                clean_lines.append(line)
            else:
                offset_adjustments.append(i)
        elif stripped_line.endswith("*/"):
            in_block_comment = False
            if any(annotation <= i + 1 for annotation in annotations):
                clean_lines.append(line)
            else:
                offset_adjustments.append(i)
        elif in_block_comment or stripped_line.startswith("//"):
            if any(annotation <= i + 1 for annotation in annotations):
                clean_lines.append(line)
            else:
                offset_adjustments.append(i)
        else:
            clean_lines.append(line)

    updated_annotations = []
    for annotation in annotations:
        adjustment = sum(1 for offset in offset_adjustments if offset < annotation)
        updated_annotations.append(annotation - adjustment)

    code = "\n".join(clean_lines)
    return remove_comments(code), updated_annotations

def generate_prompt(vulnerability_type, solidity_code):
    prompt_template = """
    You are given a piece of Solidity code. Your task is to analyze this code for vulnerabilities of a specified type.
    The type of vulnerability you need to look for is provided at the beginning of this prompt.
    You must scan through the provided Solidity code and identify any instance(s) of this vulnerability.
    Respond with the line number(s) at which each identified vulnerability instances. If multiple instances are found, separate the line numbers with a comma (e.g., "10,20,30"). Do not include whitespace between numbers.
    If no instances of the specified vulnerability are found, respond with "None".
    Vulnerability Type to Search For: {vulnerability_type} which refers to issues arising from the way arithmetic operations (like addition, subtraction, multiplication, and division) are handled, potentially leading to overflow or underflow. This occurs when an operation results in a number exceeding the maximum or minimum size that can be stored within a variable's data type, altering the intended logic or value in a contract.
    ### Solidity code:
    {solidity_code}
    ### Vulnerable lines:
    """
    return prompt_template.format(vulnerability_type=vulnerability_type, solidity_code=solidity_code)

def process_directory(repo_path, output_file, cleaned_dataset_path, output_folder):
    vulnerability_folders = [
        "access_control", "arithmetic", "bad_randomness", "denial_of_service",
        "front_running", "other", "reentrancy", "short_addresses",
        "time_manipulation", "unchecked_low_level_calls"
    ]

    all_prompts = []

    if not os.path.exists(cleaned_dataset_path):
        os.makedirs(cleaned_dataset_path)

    if not os.path.exists(output_folder):
        os.makedirs(output_folder)

    for folder in vulnerability_folders:
        folder_path = os.path.join(repo_path, 'dataset', folder)
        cleaned_folder_path = os.path.join(cleaned_dataset_path, folder)
        if not os.path.exists(cleaned_folder_path):
            os.makedirs(cleaned_folder_path)

        for file_name in os.listdir(folder_path):
            if file_name.endswith('.sol'):
                file_path = os.path.join(folder_path, file_name)
                try:
                    with open(file_path, 'r', encoding='utf-8') as file:
                        solidity_code = file.read()
                        annotations = extract_annotations(solidity_code)
                        clean_code, updated_annotations = remove_comments_and_update_lines(solidity_code, annotations)
                        # Remove blank lines
                        clean_code = "\n".join([line for line in clean_code.splitlines() if line.strip() != ""])
                        formatted_code = "\n".join([f"{i+1}: {line}" for i, line in enumerate(clean_code.splitlines())])
                        prompt = generate_prompt(folder.upper(), formatted_code)
                        all_prompts.append({
                            "file": file_name,
                            "folder": folder,
                            "prompt": prompt,
                            "annotations": updated_annotations
                        })

                        # Save cleaned Solidity code
                        cleaned_file_path = os.path.join(cleaned_folder_path, file_name)
                        with open(cleaned_file_path, 'w', encoding='utf-8') as cleaned_file:
                            cleaned_file.write(clean_code)

                except UnicodeDecodeError as e:
                    print(f"Error reading {file_path}: {e}")

    prompts_json_path = os.path.join(output_folder, 'prompts.json')
    with open(prompts_json_path, 'w', encoding='utf-8') as out_file:
        json.dump(all_prompts, out_file, indent=4)

    # Save prompts to a CSV file using pandas
    df = pd.DataFrame(all_prompts)
    df = df[['file', 'folder', 'annotations']]
    prompts_csv_path = os.path.join(output_folder, 'prompts.csv')
    df.to_csv(prompts_csv_path, index=False)

# Get the path of the current script
current_script_path = Path(__file__).resolve()
# Get the repository path (assuming the script is directly within the repo)
repo_path = current_script_path.parent.parent
# Define the other paths based on the repository path
output_folder = repo_path / 'outputs'
cleaned_dataset_path = repo_path / 'cleaned_dataset'
# Convert the paths to strings (if needed)
repo_path = str(repo_path)
output_folder = str(output_folder)
cleaned_dataset_path = str(cleaned_dataset_path)
process_directory(repo_path, output_folder, cleaned_dataset_path, output_folder)

process_directory(repo_path, output_folder, cleaned_dataset_path, output_folder)

# Read the prompts from the generated file
with open(os.path.join(output_folder, 'prompts.json'), 'r', encoding='utf-8') as file:
    prompts = json.load(file)

print(prompts[0]['prompt'])
print(prompts[0]['annotations'])
