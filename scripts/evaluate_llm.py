import json
from collections import defaultdict
import os
import pandas as pd
from pathlib import Path

def load_predictions(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        return json.load(file)

def extract_line_numbers(text):
    import re
    line_numbers = re.findall(r'\d+', text)
    return list(map(int, line_numbers))

def calculate_precision_recall(predicted, ground_truth):
    true_positives = len(set(predicted) & set(ground_truth))
    false_positives = len(set(predicted) - set(ground_truth))
    false_negatives = len(set(ground_truth) - set(predicted))
    
    precision = true_positives / (true_positives + false_positives) if (true_positives + false_positives) > 0 else 0
    recall = true_positives / (true_positives + false_negatives) if (true_positives + false_negatives) > 0 else 0
    
    return precision, recall

def evaluate_predictions(input_file, output_file):
    predictions_data = load_predictions(input_file)
    results = []

    overall_true_positives = 0
    overall_false_positives = 0
    overall_false_negatives = 0

    type_stats = defaultdict(lambda: {'true_positives': 0, 'false_positives': 0, 'false_negatives': 0})

    for entry in predictions_data:
        file_name = entry["file"]
        folder = entry["folder"]
        prediction_text = entry["prediction"]
        ground_truth = entry["annotations"]

        predicted_lines = extract_line_numbers(prediction_text)

        precision, recall = calculate_precision_recall(predicted_lines, ground_truth)

        true_positives = len(set(predicted_lines) & set(ground_truth))
        false_positives = len(set(predicted_lines) - set(ground_truth))
        false_negatives = len(set(ground_truth) - set(predicted_lines))

        overall_true_positives += true_positives
        overall_false_positives += false_positives
        overall_false_negatives += false_negatives

        type_stats[folder]['true_positives'] += true_positives
        type_stats[folder]['false_positives'] += false_positives
        type_stats[folder]['false_negatives'] += false_negatives

        results.append({
            "file": file_name,
            "folder": folder,
            "predicted_lines": predicted_lines,
            "ground_truth": ground_truth,
            "precision": precision,
            "recall": recall
        })

    overall_precision = overall_true_positives / (overall_true_positives + overall_false_positives) if (overall_true_positives + overall_false_positives) > 0 else 0
    overall_recall = overall_true_positives / (overall_true_positives + overall_false_negatives) if (overall_true_positives + overall_false_negatives) > 0 else 0

    type_results = {}
    for vulnerability_type, stats in type_stats.items():
        tp = stats['true_positives']
        fp = stats['false_positives']
        fn = stats['false_negatives']
        precision = tp / (tp + fp) if (tp + fp) > 0 else 0
        recall = tp / (tp + fn) if (tp + fn) > 0 else 0
        type_results[vulnerability_type] = {
            "precision": precision,
            "recall": recall
        }

    overall_results = {
        "overall_precision": overall_precision,
        "overall_recall": overall_recall,
        "type_results": type_results
    }

    print(f"Overall Precision: {overall_precision:.2f}")
    print(f"Overall Recall: {overall_recall:.2f}")

    with open(output_file, 'w', encoding='utf-8') as out_file:
        json.dump(results, out_file, indent=4)
    
    with open('overall_results.json', 'w', encoding='utf-8') as out_file:
        json.dump(overall_results, out_file, indent=4)

    # Save results to a CSV file using pandas
    df = pd.DataFrame(results)
    prompts_csv_path = os.path.join(output_folder, 'evaluation_results.csv')
    df.to_csv(prompts_csv_path, index=False)

    evaluation_aggregation = [{
        "vulnerability_type": 'overall',
        "precision": overall_precision,
        "recall": overall_recall
    }]

    for vulnerability_type, result in type_results.items():
        evaluation_aggregation.append({
            "vulnerability_type": vulnerability_type,
            "precision": result['precision'],
            "recall": result['recall']
        })


    
    df = pd.DataFrame(evaluation_aggregation)
    prompts_csv_path = os.path.join(output_folder, 'evaluation_aggregation.csv')
    df.to_csv(prompts_csv_path, index=False)



# Usage
input_file = 'predictions.json'  # The file containing the GPT-4 predictions
output_file = 'evaluation_results.json'  # The file where detailed results will be saved

# Get the path of the current script
current_script_path = Path(__file__).resolve()
# Get the repository path (assuming the script is directly within the repo)
repo_path = current_script_path.parent.parent
# Define the other paths based on the repository path
output_folder = repo_path / 'outputs'
output_folder = str(output_folder)

evaluate_predictions(input_file, output_file)
