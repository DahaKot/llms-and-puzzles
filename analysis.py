import os
from collections import Counter

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd  # type: ignore
from scipy import stats  # type: ignore
import json


def plot_solved_by_type(dataset, predictions_filename):
    types = []
    for example in dataset:
        types.append(example["type"])
    counted_types = Counter(types)

    correct_count, total_count = 0, 0
    i = 0
    results = {}
    for task in counted_types.keys():
        results[task] = 0

    solving_given_puzzle = True

    # for not logic
    with open(predictions_filename, 'r') as file:
        for line in file:
            if line.startswith('Counted?'):
                # Split the line to extract the value (True/False)
                if "True" in line and solving_given_puzzle:
                    correct_count += 1
                    results[types[i]] += 1

                total_count += 1
                i += 1
                solving_given_puzzle = True

    # # Read the JSON file
    # with open(predictions_filename, 'r') as f:
    #     json_data = json.load(f)

    # # Extract the "is_correct" field from the "results" list
    # counts = [1 if item.get("is_correct", False) else 0 
    #           for item in json_data["results"]]

    # for is_correct, puzzle_type in zip(counts, types):
    #     if is_correct:
    #         results[puzzle_type] += 1

    results_percentage = {}
    for puzzle_type in results:
        results_percentage[puzzle_type] = results[puzzle_type] \
            / counted_types[puzzle_type]

    # plt.rcParams.update({'font.size': 18})

    # Extract categories and their respective accuracies
    # categories = list(results.keys())

    # correctly_solved = list(results.values())
    # correctly_solved = counts

    # Plot the bar chart
    # plt.figure(figsize=(10, 6))
    # plt.bar(
    #     categories, counted_types.values(), color='coral', edgecolor='black'
    # )
    # plt.bar(
    #     categories, correctly_solved, color='skyblue', edgecolor='black',
    #     label="correctly solved"
    # )

    # # Add labels and title
    # plt.xlabel('Categories')
    # plt.ylabel('Number of Puzzles')
    # plt.title('Puzzles Solved Across Categories', fontsize=16)
    # plt.ylim(0, max(counted_types.values()) * 1.1)

    # # Add value annotations on bars
    # for i, value in enumerate(correctly_solved):
    #     plt.text(i, value / 2 - value * 0.22, f"{value}", ha='center')

    # for i, value in enumerate(counted_types.values()):
    #     plt.text(i, value + value * 0.03, f"{value}", ha='center')

    # plt.tight_layout()
    # plt.legend()
    # plt.xticks(rotation=45, ha='right')
    # # plt.subplots_adjust(bottom=0.3)

    # plt.savefig(prefix + plot_filename + "_" + predicitons_filename + ".pdf")
    # plt.savefig(prefix + plot_filename + "_" + predicitons_filename + ".png")
    # plt.show()

    return results, results_percentage


def analyze_prompt_performance(results_df):
    """
    Analyze how different prompts perform across problems

    Parameters:
    results_df: DataFrame with problems as rows, prompts as columns, and 1/0
    for success/failure

    Returns:
    Dictionary of analysis results
    """
    prompt_ids = results_df.columns
    problem_ids = results_df.index
    num_prompts = len(prompt_ids)
    num_problems = len(problem_ids)

    # Calculate basic statistics
    solved_by_prompt = results_df.sum()
    problems_solved = results_df.sum(axis=1)

    # Problems solved by at least one prompt vs. unsolved by any
    solved_by_any = (problems_solved > 0).sum()
    solved_by_none = num_problems - solved_by_any

    # Calculate pairwise relationships
    overlap_matrix = np.zeros((num_prompts, num_prompts))
    sign_test_matrix = np.zeros((num_prompts, num_prompts))
    p_value_matrix = np.zeros((num_prompts, num_prompts))
    containment_matrix = np.zeros((num_prompts, num_prompts))

    for i, prompt1 in enumerate(prompt_ids):
        for j, prompt2 in enumerate(prompt_ids):
            # Get success/failure vectors for both prompts
            prompt1_results = results_df[prompt1].values
            prompt2_results = results_df[prompt2].values

            # Overlap calculation
            overlap_matrix[i, j] = np.sum(
                (prompt1_results == 1) & (prompt2_results == 1)
            )

            # Containment: how much of prompt1 is contained in prompt2
            prompt1_successes = np.sum(prompt1_results == 1)
            containment_matrix[i, j] = \
                overlap_matrix[i, j] / prompt1_successes \
                if prompt1_successes > 0 else 0

            # Sign test calculation
            # We're interested in cases where the prompts disagreed
            pos = np.sum((prompt1_results == 1) & (prompt2_results == 0))
            neg = np.sum((prompt1_results == 0) & (prompt2_results == 1))

            # For the diagonal, set p-value to 1 (same prompt)
            if i == j:
                p_value_matrix[i, j] = 1.0
            else:
                total = pos + neg
                if total > 0:
                    # Calculate p-value for two-sided sign test
                    bin_test_result = stats.binomtest(
                        pos, n=total, p=0.5, alternative='two-sided'
                    )
                    p_value_matrix[i, j] = bin_test_result.pvalue

                    if pos > neg:
                        sign_test_matrix[i, j] = pos / total
                    else:
                        sign_test_matrix[i, j] = -neg / total
                else:
                    # No disagreements, prompts performed identically
                    p_value_matrix[i, j] = 1.0
                    sign_test_matrix[i, j] = 0

    # Find unique problems solved by each prompt
    unique_problems = {}
    for prompt in prompt_ids:
        # Problems solved by this prompt
        solved_by_this = set(results_df.index[results_df[prompt] == 1])

        # Problems solved by all other prompts
        solved_by_others = set()
        for other_prompt in prompt_ids:
            if other_prompt != prompt:
                solved_by_others.update(
                    results_df.index[results_df[other_prompt] == 1]
                )

        # Unique problems are those solved by this prompt but no others
        unique_problems[prompt] = solved_by_this - solved_by_others

    return {
        "solved_by_prompt": solved_by_prompt,
        "problems_solved": problems_solved,
        "solved_by_any": solved_by_any,
        "solved_by_none": solved_by_none,
        "overlap_matrix": overlap_matrix,
        "sign_test_matrix": sign_test_matrix,
        "p_value_matrix": p_value_matrix,
        "containment_matrix": containment_matrix,
        "unique_problems": unique_problems
    }


def visualize_prompt_performance(results_df, analysis_results, log_path):
    """
    Create visualizations of prompt performance analysis

    Parameters:
    results_df: DataFrame with problems as rows, prompts as columns, and 1/0
    for success/failure
    analysis_results: Dictionary from analyze_prompt_performance
    """
    prompt_ids = results_df.columns
    num_prompts = len(prompt_ids)

    # Create a figure
    fig = plt.figure(figsize=(20, 20))

    # Create a custom colormap for significance levels
    # Colors for different significance thresholds
    # >0.05 (not significant), ≤0.05, ≤0.01, ≤0.001
    # White, Light blue, Medium blue, Navy
    colors = ['#FFFFFF', '#ADD8E6', '#4682B4', '#000080']

    # Create a mask for statistically significant values at different levels
    p_values = analysis_results["p_value_matrix"]
    sign_values = analysis_results["sign_test_matrix"]

    annot_matrix = np.empty_like(sign_values, dtype=object)

    # Calculate Bonferroni correction
    num_comparisons = num_prompts * (num_prompts - 1) // 2
    bonferroni_alpha_001 = 0.001 / num_comparisons
    bonferroni_alpha_01 = 0.01 / num_comparisons
    bonferroni_alpha_05 = 0.05 / num_comparisons

    for i in range(num_prompts):
        for j in range(num_prompts):
            pval = p_values[i, j]
            sign_val = sign_values[i, j]

            # Add stars for significance
            if pval <= bonferroni_alpha_001:
                stars = "***†"  # Significant even with Bonferroni correction
            elif pval <= bonferroni_alpha_01:
                stars = "**†"   # Significant even with Bonferroni correction
            elif pval <= bonferroni_alpha_05:
                stars = "*†"    # Significant even with Bonferroni correction
            elif pval <= 0.001:
                stars = "***"   # Significant without correction
            elif pval <= 0.01:
                stars = "**"    # Significant without correction
            elif pval <= 0.05:
                stars = "*"     # Significant without correction
            else:
                stars = ""      # Not significant

            # Format as percent with sign
            if i == j:
                # Diagonal case - no significance test
                annot_matrix[i, j] = "—"
            else:
                if sign_val >= 0:
                    formatted_value = f"+{sign_val:.2f}{stars}"
                else:
                    formatted_value = f"{sign_val:.2f}{stars}"
                # if sign_val >= 0:
                #     formatted_value = f"+{pval:.2f}{stars}"
                # else:
                #     formatted_value = f"{pval:.2f}{stars}"
                annot_matrix[i, j] = formatted_value

    # Create color matrix based on p-values
    color_matrix = np.zeros_like(p_values)
    for i in range(num_prompts):
        for j in range(num_prompts):
            if i == j:
                # Diagonal - no test
                color_matrix[i, j] = 0  # White/no color
            elif p_values[i, j] <= 0.001:
                color_matrix[i, j] = 3  # Highly significant - Navy
            elif p_values[i, j] <= 0.01:
                color_matrix[i, j] = 2  # Very significant - Medium blue
            elif p_values[i, j] <= 0.05:
                color_matrix[i, j] = 1  # Significant - Light blue
            else:
                color_matrix[i, j] = 0  # Not significant - White

    # Create a custom colormap
    cmap = plt.matplotlib.colors.ListedColormap(colors)

    # Plot the heatmap with annotations
    ax = plt.subplot(1, 1, 1)
    im = ax.imshow(color_matrix, cmap=cmap, vmin=0, vmax=3)

    # Add annotations
    for i in range(num_prompts):
        for j in range(num_prompts):
            _ = ax.text(
                j, i, annot_matrix[i, j], ha="center", va="center",
                color="black" if color_matrix[i, j] <= 1 else "white",
                fontsize=10
            )

    # Set tick labels
    ax.set_xticks(np.arange(num_prompts))
    ax.set_yticks(np.arange(num_prompts))
    ax.set_xticklabels([id[8:-4] for id in prompt_ids])
    ax.set_yticklabels([id[8:-4] for id in prompt_ids])

    # Rotate x tick labels and set alignment
    plt.setp(
        ax.get_xticklabels(), rotation=45, ha="right", rotation_mode="anchor"
    )

    # Add a title and a legend
    ax.set_title("Sign Test Results Between Prompts")

    # Add a colorbar legend
    cbar = plt.colorbar(im, ticks=[0, 1, 2, 3])
    cbar.set_ticklabels(
        ['p > 0.05', 'p ≤ 0.05 (*)', 'p ≤ 0.01 (**)', 'p ≤ 0.001 (***)']
    )

    # Add axis labels to explain how to read the matrix
    ax.set_xlabel("Prompt B")
    ax.set_ylabel("Prompt A")

    font_size = 15

    # Add an explanation text box
    textstr = '''Positive value: Prompt A outperforms Prompt B\n \
        Negative value: Prompt B outperforms Prompt A\n\n \
        Value represents proportion of disagreements\n \
        * p≤0.05, ** p≤0.01, *** p≤0.001\n \
        † Significant after Bonferroni correction'''
    props = dict(boxstyle='round', facecolor='wheat', alpha=0.5)
    ax.text(-0.1, -0.15, textstr, transform=ax.transAxes, fontsize=font_size,
            verticalalignment='top', bbox=props, horizontalalignment='center')

    # Set font sizes for different elements
    plt.rcParams.update({'font.size': font_size})  # Set base fontsize globally

    # Adjust specific element font sizes
    ax.set_title("Sign Test Results Between Prompts", fontsize=font_size)
    ax.set_xlabel("Prompt B", fontsize=font_size)
    ax.set_ylabel("Prompt A", fontsize=font_size)

    # Adjust tick label font sizes
    ax.tick_params(axis='both', which='major', labelsize=font_size)

    # Adjust colorbar label font size
    cbar.ax.tick_params(labelsize=font_size)

    plt.tight_layout()
    plt.savefig(log_path + "_sign_test_heatmap.pdf")
    return fig


# Function to generate a detailed report
def generate_performance_report(results_df, analysis_results):
    """
    Generate a detailed textual report of the prompt performance analysis

    Parameters:
    results_df: DataFrame with problems as rows, prompts as columns, and 1/0
    for success/failure
    analysis_results: Dictionary from analyze_prompt_performance

    Returns:
    Detailed report as a string
    """
    prompt_ids = results_df.columns
    num_problems = len(results_df)

    report = []
    report.append("# Prompt Performance Analysis Report\n")

    # Overview statistics
    report.append("## Overview Statistics")
    report.append(f"- Total problems in dataset: {num_problems}")
    report.append("- Problems solved by at least one prompt: "
                  + f"{analysis_results['solved_by_any']} "
                  + f"({analysis_results['solved_by_any']/num_problems:.1%})")
    report.append("- Problems not solved by any prompt: "
                  + f"{analysis_results['solved_by_none']} "
                  + f"({analysis_results['solved_by_none']/num_problems:.1%})")
    report.append("")

    # Find prompts that are significantly better than all others
    # (with Bonferroni correction)
    report.append("## Dominant Prompts")
    p_values = analysis_results["p_value_matrix"]
    sign_values = analysis_results["sign_test_matrix"]

    # Calculate Bonferroni correction factor
    num_prompts = len(prompt_ids)
    num_comparisons = num_prompts * (num_prompts - 1) // 2
    bonferroni_alpha = 0.05 / num_comparisons

    report.append("Using Bonferroni correction for multiple testing "
                  + f"(adjusted α = {bonferroni_alpha:.6f}):")

    for i, prompt in enumerate(prompt_ids):
        # Check if this prompt is significantly better than all others
        is_dominant = True
        dominates = []
        dominates_bonferroni = []

        for j, other_prompt in enumerate(prompt_ids):
            if i != j:  # Skip comparison with self
                # Check if prompt i is significantly better than prompt j
                if sign_values[i, j] > 0 and p_values[i, j] <= 0.05:
                    dominates.append(other_prompt)
                    # Also check with Bonferroni correction
                    if p_values[i, j] <= bonferroni_alpha:
                        dominates_bonferroni.append(other_prompt)
                else:
                    is_dominant = False

        if is_dominant and dominates:
            report.append(f"- **{prompt}** is statistically significantly"
                          + " better than ALL other prompts"
                          + "(uncorrected p ≤ 0.05)")
            if len(dominates_bonferroni) == len(prompt_ids) - 1:
                report.append("  - This result holds even after Bonferroni"
                              + "correction")
            elif dominates_bonferroni:
                report.append("  - After Bonferroni correction, it is still"
                              + "significantly better than: "
                              + f"{', '.join(dominates_bonferroni)}")
            else:
                report.append("  - However, no comparisons remain significant"
                              + "after Bonferroni correction")
        elif dominates:
            report.append(f"- **{prompt}** is statistically significantly"
                          + "better than the following prompts"
                          + f"(uncorrected p ≤ 0.05): {', '.join(dominates)}")
            if dominates_bonferroni:
                report.append("  - After Bonferroni correction, it is still"
                              + "significantly better than:"
                              + f"{', '.join(dominates_bonferroni)}")
            else:
                report.append("  - However, no comparisons remain significant"
                              + "after Bonferroni correction")

    report.append("")

    # Performance by prompt
    report.append("## Performance by Prompt")
    for prompt in prompt_ids:
        solved = analysis_results["solved_by_prompt"][prompt]
        report.append(
            f"- {prompt}: Solved {solved} problems ({solved/num_problems:.1%})"
        )
    report.append("")

    # Unique problems per prompt
    report.append("## Unique Problems Solved by Each Prompt")
    for prompt in prompt_ids:
        unique = analysis_results["unique_problems"][prompt]
        report.append(f"- {prompt}: {len(unique)} unique problems"
                      + f"({len(unique) / num_problems:.1%})")
        if len(unique) <= 5:  # List them if there are only a few
            if len(unique) > 0:
                report.append(
                    f"  - Problems: {', '.join(str(p) for p in unique)}"
                )
            else:
                report.append("  - No unique problems")
    report.append("")

    # Pairwise comparisons
    report.append("## Pairwise Comparisons")
    for i, prompt1 in enumerate(prompt_ids):
        for j, prompt2 in enumerate(prompt_ids):
            if i < j:  # Avoid duplicates
                p_value = analysis_results["p_value_matrix"][i, j]
                sign_val = analysis_results["sign_test_matrix"][i, j]
                contain1in2 = analysis_results["containment_matrix"][i, j]
                contain2in1 = analysis_results["containment_matrix"][j, i]

                report.append(f"### {prompt1} vs {prompt2}")

                # Sign test results
                if sign_val > 0:
                    direction = f"{prompt1} outperforms {prompt2}"
                elif sign_val < 0:
                    direction = f"{prompt2} outperforms {prompt1}"
                else:
                    direction = "No difference in performance"

                significance = ""
                if p_value <= 0.001:
                    significance = "*** (p ≤ 0.001, highly significant)"
                elif p_value <= 0.01:
                    significance = "** (p ≤ 0.01, very significant)"
                elif p_value <= 0.05:
                    significance = "* (p ≤ 0.05, significant)"
                else:
                    significance = "(p > 0.05, not statistically significant)"

                report.append(f"- Sign test: {direction}, {significance}")
                report.append(f"- Sign test value: {abs(sign_val):.2f}"
                              + f"({abs(sign_val)*100:.1f}% of disagreements)")
                report.append(f"- {prompt1} contained in {prompt2}:"
                              + f"{contain1in2:.2f}")
                report.append(f"- {prompt2} contained in {prompt1}:"
                              + f"{contain2in1:.2f}")

                # Interpret the relationship
                if contain1in2 > 0.9:
                    report.append(f"- Almost all problems solved by {prompt1}"
                                  + f"are also solved by {prompt2}")
                elif contain1in2 > 0.7:
                    report.append(f"- Most problems solved by {prompt1} are"
                                  + f"also solved by {prompt2}")

                if contain2in1 > 0.9:
                    report.append(f"- Almost all problems solved by {prompt2}"
                                  + f"are also solved by {prompt1}")
                elif contain2in1 > 0.7:
                    report.append(f"- Most problems solved by {prompt2} are"
                                  + f"also solved by {prompt1}")

                if contain1in2 < 0.3 and contain2in1 < 0.3:
                    report.append(f"- {prompt1} and {prompt2} solve largely"
                                  + "different sets of problems")

                report.append("")

    return "\n".join(report)


def run_complete_analysis(results_df, log_path):
    """Run the complete analysis with visualizations and report"""

    analysis_results = analyze_prompt_performance(results_df)

    fig = visualize_prompt_performance(results_df, analysis_results, log_path)

    report = generate_performance_report(results_df, analysis_results)

    return {
        "results_df": results_df,
        "analysis_results": analysis_results,
        "figure": fig,
        "report": report
    }


def process_files(directory, model):
    # Get a list of all files in the directory
    files = [f for f in os.listdir(directory)
             if f.endswith('.txt') and f.startswith(model)
             and os.path.isfile(os.path.join(directory, f))]

    # Initialize a dictionary to store data for the DataFrame
    data = {}

    for file_index, file_name in enumerate(files):
        file_path = os.path.join(directory, file_name)

        # Read the file line by line
        with open(file_path, 'r') as f:
            lines = f.readlines()

        # Extract lines starting with "Counted?"
        counted_lines = [
            line.strip() for line in lines if line.startswith("Counted?")
        ]

        # Map "True" to 1 and "False" to 0
        counts = [1 if "True" in line else 0 for line in counted_lines]

        # Add the counts as a column for the current file
        data[file_name] = counts

    # Determine the maximum number of lines across all files
    max_lines = max(len(counts) for counts in data.values())

    # Ensure all columns have the same number of rows by padding with NaN
    for file_name in data:
        while len(data[file_name]) < max_lines:
            data[file_name].append(None)  # Use None for missing values

    # Create a DataFrame
    df = pd.DataFrame(data)

    return df


def process_files_json(directory, model):
    # Get a list of all JSON files in the directory
    files = [f for f in os.listdir(directory)
             if f.endswith('full.json') and f.startswith(model)
             and os.path.isfile(os.path.join(directory, f))]

    # Initialize a dictionary to store data for the DataFrame
    data = {}

    for file_index, file_name in enumerate(files):
        file_path = os.path.join(directory, file_name)

        # Read the JSON file
        with open(file_path, 'r') as f:
            json_data = json.load(f)

        # Extract the "is_correct" field from the "results" list
        if "results" in json_data:
            counts = [1 if item.get("is_correct", False) else 0
                      for item in json_data["results"]]
        else:
            counts = []

        # Add the counts as a column for the current file
        data[file_name] = counts

    # Determine the maximum number of entries across all files
    max_entries = max(len(counts) for counts in data.values()) if data else 0

    # Ensure all columns have the same number of rows by padding with NaN
    for file_name in data:
        while len(data[file_name]) < max_entries:
            data[file_name].append(None)  # Use None for missing values

    # Create a DataFrame
    df = pd.DataFrame(data)

    return df


# Main function to be called with your data
def analyze_prompt_effectiveness(
        directory, log_path, model, problem_ids=None, prompt_ids=None):
    """
    Main entry point for analyzing prompt effectiveness

    Parameters:
    df: Either a DataFrame or dictionary mapping
        {problem_id: {prompt_id: 1 or 0}}
    problem_ids: List of problem IDs (optional if df provided)
    prompt_ids: List of prompt IDs (optional if df provided)

    Returns:
    Complete analysis results
    # """
    # df = process_files(directory, model)
    df = process_files(directory, model)

    # Optionally, save the DataFrame to a CSV file
    df.to_csv(log_path + ".csv", index=False)

    new_order = [
        # "llama_base.txt", "llama_advanced.txt",
        # "llama_zero_shot_chain_of_thought.txt",
        # "llama_deepseek_advanced.txt",
        # "llama_deepseek_long_types.txt",
        # "llama_deepseek_short_types.txt",

        # "llama_random1.txt", "llama_random2.txt", "llama_random3.txt",
        # "llama_random4.txt", "llama_random5.txt",
        # "llama_semantic_random1.txt", "llama_semantic_random2.txt",
        # "llama_semantic_random3.txt", "llama_semantic_random4.txt",
        # "llama_semantic_random5.txt",
        # "llama_semantic_top_to_bottom.txt", "llama_semantic_bottom_to_top.txt",
        # "llama_thematic_random1.txt", "llama_thematic_random2.txt",
        # "llama_thematic_random3.txt", "llama_thematic_random4.txt",
        # "llama_thematic_random5.txt",
        # "llama_thematic_top_to_bottom.txt", "llama_thematic_bottom_to_top.txt",
        # "llama_deepseek_solutions.txt",

        # "qwen_base.txt", "qwen_advanced.txt",
        # "qwen_zero_shot_chain_of_thought.txt",
        # "qwen_deepseek_advanced.txt",
        # "qwen_deepseek_long_types.txt",
        # "qwen_deepseek_short_types.txt",

        # "qwen_random1.txt", "qwen_random2.txt", "qwen_random3.txt",
        # "qwen_random4.txt", "qwen_random5.txt",
        # "qwen_semantic_random1.txt", "qwen_semantic_random2.txt",
        # "qwen_semantic_random3.txt", "qwen_semantic_random4.txt",
        # "qwen_semantic_random5.txt",
        # "qwen_semantic_top_to_bottom.txt", "qwen_semantic_bottom_to_top.txt",
        # "qwen_thematic_random1.txt", "qwen_thematic_random2.txt",
        # "qwen_thematic_random3.txt", "qwen_thematic_random4.txt",
        # "qwen_thematic_random5.txt",
        # "qwen_thematic_top_to_bottom.txt", "qwen_thematic_bottom_to_top.txt",
        # "qwen_deepseek_solutions.txt",

        # "mixtral_base.txt", "mixtral_advanced.txt",
        # "mixtral_zero_shot_chain_of_thought.txt",
        # "mixtral_deepseek_advanced.txt",
        # "mixtral_deepseek_long_types.txt",
        # "mixtral_deepseek_short_types.txt",

        "mixtral_random1.txt", "mixtral_random2.txt", "mixtral_random3.txt",
        "mixtral_random4.txt", "mixtral_random5.txt",
        "mixtral_semantic_random1.txt", "mixtral_semantic_random2.txt",
        "mixtral_semantic_random3.txt", "mixtral_semantic_random4.txt",
        "mixtral_semantic_random5.txt",
        "mixtral_semantic_top_to_bottom.txt",
        "mixtral_semantic_bottom_to_top.txt",
        "mixtral_thematic_random1.txt", "mixtral_thematic_random2.txt",
        "mixtral_thematic_random3.txt", "mixtral_thematic_random4.txt",
        "mixtral_thematic_random5.txt",
        "mixtral_thematic_top_to_bottom.txt",
        "mixtral_thematic_bottom_to_top.txt",
        "mixtral_deepseek_solutions.txt",

        # that's for logic puzzles
        # "llama_base_accuracy_full.json", "llama_advanced_accuracy_full.json",
        # "llama_zero_shot_chain_of_thought_accuracy_full.json",
        # "llama_deepseek_advanced_accuracy_full.json",
        # "llama_deepseek_long_types_accuracy_full.json",
        # "llama_deepseek_short_types_proper_prompt_accuracy_full.json",

        # "llama_random1_accuracy_full.json", "llama_random2_accuracy_full.json",
        # "llama_random3_accuracy_full.json", "llama_random4_accuracy_full.json",
        # "llama_random5_accuracy_full.json",
        # "llama_semantic_random1_accuracy_full.json",
        # "llama_semantic_random2_accuracy_full.json",
        # "llama_semantic_random3_accuracy_full.json",
        # "llama_semantic_random4_accuracy_full.json",
        # "llama_semantic_random5_accuracy_full.json",
        # "llama_semantic_top_to_bottom_accuracy_full.json",
        # "llama_semantic_bottom_to_top_accuracy_full.json",
        # "llama_thematic_random1_accuracy_full.json",
        # "llama_thematic_random2_accuracy_full.json",
        # "llama_thematic_random3_accuracy_full.json",
        # "llama_thematic_random4_accuracy_full.json",
        # "llama_thematic_random5_accuracy_full.json",
        # "llama_thematic_top_to_bottom_accuracy_full.json",
        # "llama_thematic_bottom_to_top_accuracy_full.json",
        # "llama_deepseek_solutions_accuracy_full.json",

        # "qwen_base_accuracy_full.json", "qwen_advanced_accuracy_full.json",
        # "qwen_zero_shot_chain_of_thought_accuracy_full.json",
        # "qwen_deepseek_advanced_accuracy_full.json",
        # "qwen_deepseek_long_types_accuracy_full.json",
        # "qwen_deepseek_short_types_proper_prompt_accuracy_full.json",


        # "qwen_random1_accuracy_full.json", "qwen_random2_accuracy_full.json", "qwen_random3_accuracy_full.json",
        # "qwen_random4_accuracy_full.json", "qwen_random5_accuracy_full.json",
        # "qwen_semantic_random1_accuracy_full.json", "qwen_semantic_random2_accuracy_full.json",
        # "qwen_semantic_random3_accuracy_full.json", "qwen_semantic_random4_accuracy_full.json",
        # "qwen_semantic_random5_accuracy_full.json",
        # "qwen_semantic_top_to_bottom_accuracy_full.json", "qwen_semantic_bottom_to_top_accuracy_full.json",
        # "qwen_thematic_random1_accuracy_full.json", "qwen_thematic_random2_accuracy_full.json",
        # "qwen_thematic_random3_accuracy_full.json", "qwen_thematic_random4_accuracy_full.json",
        # "qwen_thematic_random5_accuracy_full.json",
        # "qwen_thematic_top_to_bottom_accuracy_full.json", "qwen_thematic_bottom_to_top_accuracy_full.json",
        # "qwen_deepseek_solutions_accuracy_full.json",

        # "mixtral_base_accuracy_full.json", "mixtral_advanced_accuracy_full.json",
        # "mixtral_zero_shot_chain_of_thought_accuracy_full.json",
        # "mixtral_deepseek_advanced_accuracy_full.json",
        # "mixtral_deepseek_long_types_accuracy_full.json",
        # "mixtral_deepseek_short_types_accuracy_full.json",

        # "mixtral_random1_accuracy_full.json", "mixtral_random2_accuracy_full.json", "mixtral_random3_accuracy_full.json",
        # "mixtral_random4_accuracy_full.json", "mixtral_random5_accuracy_full.json",
        # "mixtral_semantic_random1_accuracy_full.json", "mixtral_semantic_random2_accuracy_full.json",
        # "mixtral_semantic_random3_accuracy_full.json", "mixtral_semantic_random4_accuracy_full.json",
        # "mixtral_semantic_random5_accuracy_full.json",
        # "mixtral_semantic_top_to_bottom_accuracy_full.json",
        # "mixtral_semantic_bottom_to_top_accuracy_full.json",
        # "mixtral_thematic_random1_accuracy_full.json", "mixtral_thematic_random2_accuracy_full.json",
        # "mixtral_thematic_random3_accuracy_full.json", "mixtral_thematic_random4_accuracy_full.json",
        # "mixtral_thematic_random5_accuracy_full.json",
        # "mixtral_thematic_top_to_bottom_accuracy_full.json",
        # "mixtral_thematic_bottom_to_top_accuracy_full.json",
        # "mixtral_deepseek_solutions_accuracy_full.json",
    ]

    # Rearrange columns
    df = df[new_order]

    if df is not None:
        # Check if it's already a DataFrame
        if isinstance(df, pd.DataFrame):
            results_df = df
        # Or if it's a nested dictionary
        elif isinstance(df, dict) \
                and all(isinstance(v, dict) for v in df.values()):
            # Convert from dictionary to DataFrame
            all_prompts = set().union(*[d.keys() for d in df.values()])
            results_df = pd.DataFrame.from_dict(
                {prob:
                 {prompt: df[prob].get(prompt, 0) for prompt in all_prompts}
                 for prob in df},
                orient='index'
            )
        else:
            raise TypeError(
                "df must be either a DataFrame or a nested dictionary"
            )

    return run_complete_analysis(results_df, log_path)
