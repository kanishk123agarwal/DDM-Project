import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def main():
    # 1. Loading & Displaying Data
    print("--- 1. Loading & Displaying Data ---")
    file_path = 'patient_consent.csv'
    try:
        df = pd.read_csv(file_path)
        print("Dataset loaded successfully.")
    except FileNotFoundError:
        print(f"Error: File '{file_path}' not found.")
        return

    # View initial rows and structure
    print("\nFirst 5 rows:")
    print(df.head())
    
    print("\nDataset Info:")
    print(df.info())
    
    print("\nDataset Description:")
    print(df.describe())

    # 2. Handling Missing Data
    print("\n--- 2. Handling Missing Data ---")
    # Check for missing values
    missing_values = df.isnull().sum()
    print("\nMissing values per column:")
    print(missing_values)

    # Impute missing values (Example: filling numeric columns with mean)
    # Note: The provided dataset might be clean, but this demonstrates the logic.
    numeric_cols = df.select_dtypes(include=[np.number]).columns
    if df[numeric_cols].isnull().any().any():
        print("\nImputing missing numeric values with mean...")
        df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())
        print("Missing values after imputation:")
        print(df.isnull().sum())
    else:
        print("\nNo missing numeric values to impute.")

    # 3. Handling Categorical Data
    print("\n--- 3. Handling Categorical Data ---")
    # Convert timestamp to datetime objects for better handling
    if 'timestamp' in df.columns:
        df['timestamp'] = pd.to_datetime(df['timestamp'], format='%d-%m-%Y %H:%M')
        print("\nConverted 'timestamp' to datetime objects.")
    
    # One-hot encoding (Example: 'study_id' could be categorical)
    # Using 'study_id' as an example for categorical encoding
    if 'study_id' in df.columns:
        print("\nOne-hot encoding 'study_id'...")
        df_encoded = pd.get_dummies(df, columns=['study_id'], prefix='study')
        print("\nFirst 5 rows after encoding 'study_id':")
        print(df_encoded.head())
    else:
        df_encoded = df

    # 4. Data Visualization & EDA
    print("\n--- 4. Data Visualization & EDA ---")
    
    # Histogram for numeric columns
    print("Generating histograms...")
    df.hist(figsize=(10, 8), bins=10)
    plt.tight_layout()
    plt.suptitle("Histograms of Numeric Columns", y=1.02)
    # plt.savefig('histograms.png')
    print("Saved histograms to 'histograms.png'")
    plt.show() # Commented out to prevent blocking execution

    # Correlation Heatmap
    print("Generating correlation heatmap...")
    plt.figure(figsize=(10, 8))
    # Select only numeric columns for correlation
    numeric_df = df.select_dtypes(include=[np.number])
    corr_matrix = numeric_df.corr()
    sns.heatmap(corr_matrix, annot=True, cmap='coolwarm', fmt=".2f")
    plt.title("Correlation Heatmap")
    # plt.savefig('heatmap.png')
    print("Saved heatmap to 'heatmap.png'")
    plt.show() # Commented out to prevent blocking execution

if __name__ == "__main__":
    main()
