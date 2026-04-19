import matplotlib.pyplot as plt
import numpy as np
import seaborn as sns

def generate_benchmark_graph():
    output_image = "benchmark_results.png"
    
    datasets = ['Patient Consent\n(18 records)', 'Healthcare Data\n(55,500 records)']
    times = [0.0831, 0.2917]
    
    # Create figure
    plt.figure(figsize=(8, 6))
    sns.set_theme(style="whitegrid")
    
    x = np.arange(len(datasets))
    width = 0.5
    
    fig, ax = plt.subplots(figsize=(8, 6))
    rects1 = ax.bar(x, times, width, color=['#4C72B0', '#DD8452'])
    
    ax.set_ylabel('Execution Time (Seconds)', fontsize=12)
    ax.set_title('MapReduce Scalability Performance Benchmark', fontsize=14, pad=20, fontweight='bold')
    ax.set_xticks(x)
    ax.set_xticklabels(datasets, fontsize=12)
    
    # Make y axis slightly taller to accommodate text
    ax.set_ylim(0, max(times) + 0.1)
    
    def autolabel(rects):
        for rect in rects:
            height = rect.get_height()
            ax.annotate(f'{height} sec',
                        xy=(rect.get_x() + rect.get_width() / 2, height),
                        xytext=(0, 3),
                        textcoords="offset points",
                        ha='center', va='bottom', fontsize=11, fontweight='bold')
                        
    autolabel(rects1)
    fig.tight_layout()
    
    plt.savefig(output_image, dpi=300, bbox_inches='tight')
    print(f"Benchmark graph successfully generated and saved as {output_image}")

if __name__ == "__main__":
    generate_benchmark_graph()
