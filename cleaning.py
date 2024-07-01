import re
import csv

def clean_code(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()

    cleaned_lines = []
    original_to_cleaned_line_map = {}
    vulnerability_lines = []
    in_multiline_comment = False
    cleaned_line_no = 0

    for line_no, line in enumerate(lines, start=1):
        stripped_line = line.strip()

        # Extract vulnerability line numbers from the annotation
        vulnerability_match = re.search(r'@vulnerable_at_lines: ([\d,]+)', stripped_line)
        if vulnerability_match:
            vulnerability_lines.extend(map(int, vulnerability_match.group(1).split(',')))
            continue

        # Skip single-line comments and annotations
        if stripped_line.startswith('//') or stripped_line.startswith('/*') or stripped_line.startswith('*'):
            continue

        # Handle multi-line comments
        if '/*' in stripped_line:
            in_multiline_comment = True
            continue
        if '*/' in stripped_line:
            in_multiline_comment = False
            continue
        if in_multiline_comment:
            continue

        # Skip blank lines
        if stripped_line == '':
            continue

        # Keep track of the mapping from original to cleaned line numbers
        cleaned_line_no += 1
        original_to_cleaned_line_map[line_no] = cleaned_line_no
        cleaned_lines.append(stripped_line)

    # Map the original vulnerability lines to the new cleaned line numbers
    cleaned_vulnerability_lines = [original_to_cleaned_line_map[line] for line in vulnerability_lines if line in original_to_cleaned_line_map]
    with open(r'Cleaned_Output_annotations\vulnerability_line_number.txt', 'w') as file:
        for line in cleaned_vulnerability_lines:
            file.write(f"{line}\n") 
    return cleaned_lines, cleaned_vulnerability_lines

def write_cleaned_code(cleaned_lines, output_file_path):
    with open(output_file_path, 'w') as file:
        for line in cleaned_lines:
            file.write(line + '\n')

def write_annotations_to_csv(cleaned_lines, cleaned_vulnerability_lines, csv_file_path):
    with open(csv_file_path, 'w', newline='') as csvfile:
        fieldnames = ['line_number', 'code', 'vulnerability']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)

        writer.writeheader()
        for line_no, line in enumerate(cleaned_lines, start=1):
            writer.writerow({
                'line_number': line_no,
                'code': line, 
                'vulnerability': 'yes' if line_no in cleaned_vulnerability_lines else 'no'
            })
# Function to generate highlighted code with vulnerabilities in ANSI color
def generate_highlighted_code(cleaned_lines, cleaned_vulnerability_lines, highlighted_file_path):
    with open(highlighted_file_path, 'w') as file:
        for line_no, line in enumerate(cleaned_lines, start=1):
            if line_no in cleaned_vulnerability_lines:
                file.write('\033[91m' + line + '\033[0m\n')  # ANSI escape code for red color
            else:
                file.write(line + '\n')            

def main():
    input_file_path = r'Uncleaned_Input\Input.txt'
    output_file_path = r'Cleaned_Output_annotations\cleaned_code.txt'
    csv_file_path = r'Cleaned_Output_annotations\annotations.csv'
    highlighted_output_file_path = 'Cleaned_Output_annotations\highlighted_code.txt'
    cleaned_lines, cleaned_vulnerability_lines = clean_code(input_file_path)
    write_cleaned_code(cleaned_lines, output_file_path)
    write_annotations_to_csv(cleaned_lines, cleaned_vulnerability_lines, csv_file_path)
    generate_highlighted_code(cleaned_lines, cleaned_vulnerability_lines, highlighted_output_file_path)


    print(f"Cleaned code written to {output_file_path}")
    print(f"Annotations written to {csv_file_path}")
    print(f"Vulnerabilities found at cleaned line numbers: {cleaned_vulnerability_lines}")
    print(f"Highlighted code with vulnerabilities written to {highlighted_output_file_path}")
    
if __name__ == '__main__':
    main()
