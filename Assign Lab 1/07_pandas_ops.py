import pandas as pd
import matplotlib.pyplot as plt
import os

def pandas_operations(filename):
    print(f"--- Pandas Operations on {filename} ---")
    
    # 1. Load Data
    try:
        df = pd.read_csv(filename)
        print("Data loaded successfully.")
    except Exception as e:
        print(f"Error loading CSV: {e}")
        return

    # 2. Inspect Data
    print("\n--- Head ---")
    print(df.head())
    
    print("\n--- Info ---")
    print(df.info())

    # 3. Handling Missing Data
    print("\n--- Handling Missing Data ---")
    # Check for missing values
    print(f"Missing values per column:\n{df.isnull().sum()}")
    
    # Fill missing values (if any) with 0 or drop
    # For demonstration, let's fill numeric NaNs with mean (if applicable) or 0
    df_filled = df.fillna(0)
    print("Missing values filled with 0.")

    # 4. Arithmetic Operations
    print("\n--- Arithmetic Operations ---")
    # Create a new column 'total_score' as sum of demographics + mental_health + biospecimen
    # Assuming these are numeric columns (0 or 1)
    df_filled['total_score'] = df_filled['demographics'] + df_filled['mental_health'] + df_filled['biospecimen']
    print("Created 'total_score' column.")
    print(df_filled[['patient_id', 'total_score']].head())

    # 5. Aggregation (Group By)
    print("\n--- Aggregation ---")
    # Group by study_id and calculate mean total_score
    grouped = df_filled.groupby('study_id')['total_score'].mean()
    print("Mean Total Score by Study ID:")
    print(grouped)

    # 6. Plotting
    print("\n--- Plotting ---")
    try:
        plt.figure(figsize=(10, 6))
        grouped.plot(kind='bar', color='skyblue')
        plt.title('Average Total Score by Study ID')
        plt.xlabel('Study ID')
        plt.ylabel('Average Score')
        plt.tight_layout()
        
        plot_file = 'study_scores_plot.png'
        plt.savefig(plot_file)
        print(f"Plot saved to {plot_file}")
    except Exception as e:
        print(f"Error plotting: {e}")

def main():
    pandas_operations('patient_consent.csv')

if __name__ == "__main__":
    main()
