import re
import json
import os
import pandas as pd
from IPython.display import display, HTML

def extract_model_answers_and_correct_answers(text):
    """
    Extract both model predictions and correct answers from formatted text.
    
    Handles multiple prediction formats:
    1. **solution**: [x] format
    2. answer: x format
    
    Returns a list of dictionaries with prediction details.
    """
    # Split the text into individual blocks by "Input:"
    blocks = re.split(r'Input:', text)
    blocks = [b.strip() for b in blocks if b.strip()]
    
    results = []

    
    for i, block in enumerate(blocks):
        # Skip blocks without predictions
        if "Prediction:" not in block:
            continue
            
        # Extract the prediction part
        prediction_parts = block.split("Prediction:")
        if len(prediction_parts) < 2:
            continue
            
        # The raw prediction might include system info after it
        full_prediction = prediction_parts[1].strip()
        
        # Extract only the model's prediction by stopping at system info markers
        # Look for "Correct Answer:" followed by "Counted?" which indicates system info, not prediction
        system_info_match = re.search(r'Correct Answer:\s*[A-E](?:.+?)Counted\?', full_prediction, re.DOTALL)
        if system_info_match:
            # Find the start position of the system info
            system_start = full_prediction.find(system_info_match.group(0))
            # Extract only the prediction part before system info
            prediction = full_prediction[:system_start].strip()
        else:
            # If no system info marker found, use the full prediction
            prediction = full_prediction
            
        # Extract the correct answer from the system info
        correct_answer_match = re.search(r'Correct Answer:\s*([A-E])\nCounted?', block, re.IGNORECASE)
        correct_answer = correct_answer_match.group(1).lower() if correct_answer_match else None
        
        result = {
            "prediction_number": i+1, 
            "letter_answer": None,
            "correct_answer": correct_answer,
            "is_correct": False,
            "full_solution": prediction,
            "explanation": "",
        }

        

        if prediction.startswith("puzzle:") or prediction.startswith("**puzzle"):
            # print("starts with puzzle")
            result["is_correct"] = False
            result["explanation"] = "generating new puzzle instead of answering new one"
            results.append(result)
            continue

        # Extract the letter answer using multiple patterns
        patterns = [
            # Format 1: "the correct answer is [x]"
            r"(?:the correct answer is|the answer is|correct answer:)\s*\[([a-e])\]",

            # Format 1: "the correct answer is [x]"
            r"(?:the correct answer is|the answer is|correct answer:)\n*\[([a-e])\]",
            
            # Format 2: "answer: x"
            r"^answer:\s*([a-e])\b",

            # Format 2: "answer:\nx"
            r"^answer:\n*([a-e])\b",

            # Format 2: "answer: x"
            r"^answer:\s*[\[]([a-e])\b",

            # Format 2: "answer:\n[x"
            r"^answer:\n*[\[]([a-e])\b",
            
            # Format 3: "the best answer is x"
            r"the best answer is\s*([a-e])\b",
            
            # Format 4: "choice (x) is the correct answer"
            r"choice\s*\(([a-e])\)",
            r"\(([a-e])\)\s*is\s*(?:the correct|the best|correct)",
            
            # Format 5: "therefore, [x] is the correct answer"
            r"\[([a-e])\]\s*(?:is|as|the)",
            
            # Format 6: Answer near words like "answer" or "correct"
            r"(?:answer|correct|select)(?:.{0,20})\[([a-e])\]",

            # Format 6: Answer near words like "answer" or "correct"
            r"(?:answer|correct|select)(?:.{0,20})\b([a-e])\b",

            # Format 8: Simple bracket pattern as fallback
            # r"([a-e])\n",
            # Format 7: Simple bracket pattern as fallback
            # r"\[([a-e])\]",
        ]
        
        # Try to extract from solution or full prediction
        for pattern in patterns:
            match = re.search(pattern, prediction, re.MULTILINE | re.IGNORECASE | re.DOTALL)
            if match:
                result["letter_answer"] = match.group(1).lower()
                break

        if (prediction.startswith(f"[{result["correct_answer"]}]")
                or prediction.startswith(f"{result["correct_answer"]} ")
                or prediction.startswith(f"{result["correct_answer"]}\n")):
            result["letter_answer"] = result["correct_answer"]
        
        # Extract explanation if present
        explanation_match = re.search(r"\*\*explanation\*\*:(.+?)(?:\*\*|$)", prediction, re.DOTALL)
        if explanation_match:
            result["explanation"] = explanation_match.group(1).strip()
        elif "explanation:" in prediction.lower():
            # Alternative format: explanation: text
            exp_parts = prediction.split("explanation:", 1)
            if len(exp_parts) > 1:
                result["explanation"] = exp_parts[1].strip()
        
        # Check if the model's answer matches the correct answer
        if result["letter_answer"] and result["correct_answer"]:
            result["is_correct"] = result["letter_answer"].lower() == result["correct_answer"].lower()
        
        results.append(result)
    
    return results

def calculate_accuracy(results):
    """
    Calculate the accuracy of the model's predictions.
    """
    # Filter out results without both answers
    valid_results = [r for r in results if r["letter_answer"] is not None and r["correct_answer"] is not None]
    
    if not valid_results:
        return {
            "overall_accuracy": 0,
            "correct_count": 0,
            "total_count": 0,
            "prediction_results": []
        }
    
    correct_count = sum(1 for r in valid_results if r["is_correct"])
    total_count = len(valid_results)
    overall_accuracy = (correct_count / total_count) * 100 if total_count > 0 else 0
    
    prediction_results = [
        (r["prediction_number"], r["letter_answer"], r["correct_answer"], r["is_correct"])
        for r in valid_results
    ]
    
    return {
        "overall_accuracy": overall_accuracy,
        "correct_count": correct_count,
        "total_count": total_count,
        "prediction_results": prediction_results
    }

def generate_debug_info(text, results):
    """
    Generate debug information for inspection.
    """
    debug_info = []
    
    blocks = re.split(r'Input:', text)
    blocks = [b.strip() for b in blocks if b.strip() and "Prediction:" in b]
    
    for i, block in enumerate(blocks):
        prediction_parts = block.split("Prediction:")
        if len(prediction_parts) < 2:
            continue
            
        full_prediction = prediction_parts[1].strip()
        
        # Check for system info
        system_info_match = re.search(r'Correct Answer:\s*[A-E](?:.+?)Counted\?', full_prediction, re.DOTALL)
        
        debug_entry = {
            "block_number": i+1,
            "prediction": "",
            "system_info": "",
            "extracted_answer": "",
            "correct_answer": "",
            "is_correct": False,
            "explanation": ""
        }
        
        if system_info_match:
            system_start = full_prediction.find(system_info_match.group(0))
            prediction = full_prediction[:system_start].strip()
            system_info = full_prediction[system_start:].strip()
            
            debug_entry["prediction"] = prediction
            debug_entry["system_info"] = system_info
        else:
            debug_entry["prediction"] = full_prediction
            debug_entry["system_info"] = "No system info detected"
        
        # Add extracted answer info
        result = next((r for r in results if r["prediction_number"] == i+1), None)
        if result:
            debug_entry["extracted_answer"] = result["letter_answer"]
            debug_entry["correct_answer"] = result["correct_answer"]
            debug_entry["is_correct"] = result["is_correct"]
        
        debug_info.append(debug_entry)
    
    return debug_info

def process_predictions(text_data):
    """
    Process prediction text and return structured results.
    
    Args:
        text_data: String containing predictions in the expected format
        
    Returns:
        Dictionary with results and analysis
    """
    # Extract data and calculate accuracy
    results = extract_model_answers_and_correct_answers(text_data)
    accuracy_metrics = calculate_accuracy(results)
    debug_info = generate_debug_info(text_data, results)
    
    # Create results dataframe
    df_results = pd.DataFrame([
        {
            "Prediction #": r["prediction_number"],
            "Model Answer": r["letter_answer"] or "Not found",
            "Correct Answer": r["correct_answer"] or "Not found",
            "Is Correct": "✓" if r["is_correct"] else "✗",
            "Solution Start": r["full_solution"][:100].replace("\n", " ").strip() + "..."
        }
        for r in results
    ])
    
    # Create debug dataframe
    df_debug = pd.DataFrame([
        {
            "Block #": d["block_number"],
            "Extracted Answer": d["extracted_answer"],
            "Correct Answer": d["correct_answer"],
            "Is Correct": "✓" if d["is_correct"] else "✗",
            "Prediction Start": d["prediction"][:150].replace("\n", " ").strip() + "..."
        }
        for d in debug_info
    ])
    
    # Summary statistics
    summary = {
        "total_predictions": len(results),
        "valid_predictions": accuracy_metrics["total_count"],
        "correct_predictions": accuracy_metrics["correct_count"],
        "accuracy": accuracy_metrics["overall_accuracy"],
        "results_df": df_results,
        "debug_df": df_debug,
        "full_results": results,
        # "full_debug": debug_info
    }
    
    return summary

def display_results(summary):
    """
    Display formatted results in the notebook.
    """
    print(f"SUMMARY STATISTICS:")
    print(f"Total predictions found: {summary['total_predictions']}")
    print(f"Valid predictions (with extractable answer and correct answer): {summary['valid_predictions']}")
    print(f"Correct predictions: {summary['correct_predictions']}")
    print(f"Overall Accuracy: {summary['accuracy']:.2f}%")
    
    print("\nRESULTS TABLE:")
    display(summary["results_df"])
    
    print("\nDEBUG INFORMATION:")
    display(summary["debug_df"])
    
    # Display mismatches if any
    mismatches = summary["results_df"][summary["results_df"]["Is Correct"] == "✗"]
    if not mismatches.empty:
        print("\nMISMATCHES:")
        display(mismatches)
    else:
        print("\nNo mismatches found!")

# Main function for notebook usage
def analyze_model_predictions(file_path):
    """
    Analyze model predictions from a file.
    
    Args:
        file_path: Path to the file containing predictions
        
    Returns:
        Summary dictionary with results and displays formatted output
    """
    try:
        # print(file_path)
        # Read the file
        with open(file_path, "r", encoding="utf-8") as f:
            text_data = f.read()
        
        # Process the predictions
        summary = process_predictions(text_data)
        
        # Display results
        # display_results(summary)
        
        return summary
    
    except Exception as e:
        print(f"Error analyzing predictions: {str(e)}")
        return None

# Example usage:
# summary = analyze_model_predictions("predictions.txt")

# To save results to files:
def save_results(summary, output_prefix="analysis"):
    """
    Save results to files.
    
    Args:
        summary: Summary dictionary from analyze_model_predictions
        output_prefix: Prefix for output filenames
    """
    # # Save results CSV
    # summary["results_df"].to_csv(f"{output_prefix}_results.csv", index=False)
    # print(f"Results saved to {output_prefix}_results.csv")
    
    # # Save debug CSV
    # summary["debug_df"].to_csv(f"{output_prefix}_debug.csv", index=False)
    # print(f"Debug information saved to {output_prefix}_debug.csv")
    
    # Save full results JSON
    with open(f"{output_prefix}_full.json", "w", encoding="utf-8") as f:
        json_data = {
            "summary": {
                "total_predictions": summary["total_predictions"],
                "valid_predictions": summary["valid_predictions"],
                "correct_predictions": summary["correct_predictions"],
                "accuracy": summary["accuracy"]
            },
            "results": summary["full_results"],
        }
        json.dump(json_data, f, indent=2)
    print(f"Full data saved to {output_prefix}_full.json")

# Example usage:
# save_results(summary, "my_analysis")
    
directory = "./logs/logic_puzzles/"
# files = [f for f in os.listdir(directory)
#              if f.endswith('.txt') and "solution" in f
#              and os.path.isfile(os.path.join(directory, f))]
files = ["logic_puzzles_mixtral_deepseek_advanced.txt",
         "logic_puzzles_mixtral_deepseek_long_types.txt",
         "logic_puzzles_mixtral_deepseek_short_types.txt",
         "logic_puzzles_mixtral_deepseek_solutions.txt"]

for input_file in files:
    output_file = input_file[:-4] + "_accuracy"
    summary = analyze_model_predictions(directory + input_file)
    save_results(summary, directory + output_file)

# input_file = "./logs/logic_puzzles/llama_deepseek_short_types.txt"
# output_file = "./logs/logic_puzzles/llama_deepseek_short_types_accuracy.csv"
# results, accuracy = run_extraction_with_accuracy(input_file, output_file)
# extract_to_csv_with_accuracy(input_file)