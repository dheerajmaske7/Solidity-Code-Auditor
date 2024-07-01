import anthropic

# Replace with your actual API key
client = anthropic.Anthropic(api_key="ADD_API_KEY")

# Provide the paths to the prompt files and Solidity code file
system_prompt_path = r'Prompts\system_prompt.txt'
user_prompt_path = r'Prompts\user_prompt.txt'
solidity_code_path = r'Cleaned_Output_annotations\cleaned_code.txt'
vulnerabilities_line_number_path = r'Cleaned_Output_annotations\vulnerability_line_number.txt'

try:
    # Load the system and user prompts from the specified paths
    with open(system_prompt_path, 'r') as file:
        system_prompt = file.read()

    with open(user_prompt_path, 'r') as file:
        user_prompt_template = file.read()

    # Load the Solidity code from the specified path
    with open(solidity_code_path, 'r') as file:
        solidity_code = file.read()

    # Load vulnerability lines from the specified path
    with open(vulnerabilities_line_number_path, 'r') as file:
        # Read and strip any extra whitespace, then split by comma
        vulnerability_lines = file.read().strip().split(',')
        # Convert list elements to strings and join them with a comma
        vulnerability_lines_str = ", ".join(map(str, vulnerability_lines))
        print('vulnerability are found on the lines' + vulnerability_lines_str )

    # Replace the placeholder with the actual Solidity code and vulnerability lines
    user_prompt = user_prompt_template.replace("{{solidity_code}}", solidity_code).replace("{{vulnerability_lines}}", vulnerability_lines_str)

    # Create the message with the loaded prompts
    message = client.messages.create(
        model="claude-3-opus-20240229",
        max_tokens=1000,
        temperature=0,
        system=system_prompt,
        messages=[
            {
                "role": "user",
                "content": user_prompt
            }
        ]
    )

    if isinstance(message.content, list) and len(message.content) > 0:
        text_content = message.content[0].text  # Assuming there's only one TextBlock in the list
        print(text_content)

        # Print the evaluation to Prediction.txt
        with open('Prediction.txt', 'w') as file:
            file.write(text_content)

        print("Evaluation written to Prediction.txt")
    else:
        print("Error: Unexpected structure in message.content")

except anthropic.BadRequestError as e:
    # Catching the BadRequestError and printing the error message
    print(f"Error: {str(e)}")
    print("Please check your credit balance and try again.")
except Exception as e:
    print(f"An error occurred: {str(e)}")
