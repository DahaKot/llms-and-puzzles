import matplotlib.pyplot as plt
from collections import Counter
import os


def plot_solved_by_type(dataset, prefix, predictions_filename, plot_filename):
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

    with open(prefix + predictions_filename + ".txt", 'r') as file:
        for line in file:
            # Check if the line starts with "counted"
            if line.startswith("Prediction: puzzle:"):
                # print("solving a wrong puzzle ", types[i])
                solving_given_puzzle = False

            if line.startswith('Counted?'):
                if "True" in line and not solving_given_puzzle:
                    print("ALARM")
                # Split the line to extract the value (True/False)
                if "True" in line and solving_given_puzzle:
                    correct_count += 1
                    results[types[i]] += 1

                total_count += 1
                i += 1
                solving_given_puzzle = True

    plt.rcParams.update({'font.size': 18})

    # Extract categories and their respective accuracies
    categories = list(results.keys())
    correctly_solved = list(results.values())

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

    return correctly_solved
