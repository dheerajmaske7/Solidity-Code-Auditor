# yokai-security-auditor

## Prerequisites

1. **Python**: Ensure you have Python 3.6 or higher installed.
2. **Required Library**: Install required libraries
   ```bash
   pip install -r requirements.txt
   ```
   OpenAI API Key: Obtain your OpenAI API key from the OpenAI dashboard.

## Scripts

1. Generate Prompts (generate_prompts.py)
   This script generates prompts from the Solidity smart contracts in the repository.

2. GPT-4 Predictor (predict_vulnerability.py)
   This script sends the generated prompts to GPT-4 and collects the predictions.

3. Evaluator Script (evaluate_llm.py)
   This script evaluates the LLM predictions against the ground truth annotations using precision and recall metrics.

## Usage

Run scripts in the following orders:

```
python scripts/generate_prompt.py
python scripts/predict_vulnerability.py
python scripts/evaluate_llm.py
```

# Run the agent using docker
This project contains a Streamlit application below are the steps to run the application using docker also the application also requires an OpenAI API key.

## Requirements
- Docker 26.1.3

## Build the Docker Image
Run the following command to build the Docker image:
```bash
docker build -t yokai_security_auditor .
```
## Run the Docker Container
Run the Docker container with the following command, passing the OPENAI_API_KEY environment variable:
```bash
docker run -p 8501:8501 -e ADD_API_KEY=your_openai_api_key_here yokai_security_auditor
```