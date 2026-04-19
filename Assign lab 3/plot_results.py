import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns
import os

def generate_graph():
    # File containing the results
    input_file = "final_output.txt"
    output_image = "consent_results.png"
    
    if not os.path.exists(input_file):
        print(f"Error: {input_file} not found. Please run MapReduce simulation first.")
        return

    categories = []
    consents = []
    requests = []
    
    with open(input_file, "r") as f:
        for line in f:
            # line format example:
            # biospecimen	Consents: 10 / Total Requests: 18
            try:
                parts = line.strip().split('\t')
                category = parts[0]
                
                # Consents: 10 / Total Requests: 18
                stats = parts[1]
                consent_part, requests_part = stats.split(' / ')
                
                consent_val = int(consent_part.split(': ')[1])
                request_val = int(requests_part.split(': ')[1])
                
                categories.append(category.replace('_', ' ').title())
                consents.append(consent_val)
                requests.append(request_val)
            except Exception as e:
                print(f"Error parsing line: {line.strip()} - {e}")
                continue

    if not categories:
        print("No valid data found to plot.")
        return

    # Create figure
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    # Set up the positions for bars
    x = np.arange(len(categories))
    width = 0.35  # width of the bars

    # Plot
    fig, ax = plt.subplots(figsize=(12, 7))
    rects1 = ax.bar(x - width/2, consents, width, label='Consents Received', color='#4C72B0')
    rects2 = ax.bar(x + width/2, requests, width, label='Total Requests', color='#DD8452')

    # Add labels, title, and formatting
    ax.set_ylabel('Number of Patients', fontsize=12)
    ax.set_title('Patient Data-Sharing Consents by Category', fontsize=14, pad=20, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(categories, rotation=45, ha='right', fontsize=11)
    ax.legend(fontsize=11)

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
    autolabel(rects2)

    fig.tight_layout()
    
    # Save the figure
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    print(f"Graph successfully generated and saved as {output_image}")

if __name__ == "__main__":
    generate_graph()
