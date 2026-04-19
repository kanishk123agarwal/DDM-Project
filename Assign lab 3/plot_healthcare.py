import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

def generate_healthcare_graph():
    # File containing the results
    input_file = "final_output_healthcare.txt"
    output_image = "healthcare_results.png"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Please run MapReduce simulation first.")
        return

    conditions = []
    counts = []
    
    with open(input_file, "r") as f:
        for line in f:
            try:
                parts = line.strip().split('\t')
                condition = parts[0]
                
                # Consents: 9308 / Total Requests: 9308
                stats = parts[1]
                count_part, _ = stats.split(' / ')
                
                count_val = int(count_part.split(': ')[1])
                
                conditions.append(condition.replace('_', ' ').title())
                counts.append(count_val)
            except Exception as e:
                print(f"Error parsing line: {line.strip()} - {e}")
                continue

    if not conditions:
        print("No valid data found to plot.")
        return

    # Create figure
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    # Set up the positions for bars
    x = np.arange(len(conditions))
    width = 0.5

    # Plot
    fig, ax = plt.subplots(figsize=(12, 7))
    rects1 = ax.bar(x, counts, width, label='Frequency in Dataset', color='#55A868')

    # Add labels, title, and formatting
    ax.set_ylabel('Number of Patients', fontsize=12)
    ax.set_title('Frequency of Medical Conditions (Healthcare Dataset MapReduce)', fontsize=14, pad=20, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(conditions, rotation=45, ha='right', fontsize=11)
    
    # Set ylim slightly higher to accommodate labels
    ax.set_ylim(0, max(counts) + 1000)

    # Attach a text label above each bar displaying its height
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height}',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),  # 3 points vertical offset
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=10)

    autolabel(rects1)
    fig.tight_layout()
    
    # Save the figure
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    print(f"Graph successfully generated and saved as {output_image}")

if __name__ == "__main__":
    generate_healthcare_graph()
