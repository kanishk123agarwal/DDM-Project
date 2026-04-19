import numpy as np
import csv

def create_arrays():
    print("--- Creating Arrays ---")
    # From list
    arr1 = np.array([1, 2, 3, 4, 5])
    print(f"Array 1 (1D): {arr1}")
    
    # From range
    arr2 = np.arange(10)
    print(f"Array 2 (arange): {arr2}")
    
    # Reshape
    arr3 = arr2.reshape(2, 5)
    print(f"Array 3 (Reshaped 2x5):\n{arr3}")
    
    return arr1, arr3

def array_operations(arr1, arr3):
    print("\n--- Array Operations ---")
    # Slicing
    print(f"Slice of Array 1 (2:4): {arr1[2:4]}")
    
    # Indexing
    print(f"Element at (1, 3) in Array 3: {arr3[1, 3]}")
    
    # Arithmetic
    print(f"Array 1 + 10: {arr1 + 10}")
    print(f"Array 1 * 2: {arr1 * 2}")
    
    # Aggregation
    print(f"Sum of Array 1: {np.sum(arr1)}")
    print(f"Mean of Array 1: {np.mean(arr1)}")
    print(f"Max of Array 3 (axis 1): {np.max(arr3, axis=1)}")

def load_from_csv(filename):
    print(f"\n--- Loading Data from {filename} into NumPy ---")
    try:
        # Load only numeric columns: patient_id (0), study_id (1), demographics (3), mental_health (4)
        # Skip header
        data = np.genfromtxt(filename, delimiter=',', skip_header=1, usecols=(0, 1, 3, 4))
        print(f"Loaded shape: {data.shape}")
        print(f"First 5 rows:\n{data[:5]}")
        
        # Calculate mean of mental_health (column index 3 in our subset)
        mental_health_col = data[:, 3]
        print(f"Mean Mental Health Score: {np.mean(mental_health_col):.2f}")
        
    except Exception as e:
        print(f"Error loading CSV with numpy: {e}")

def main():
    arr1, arr3 = create_arrays()
    array_operations(arr1, arr3)
    load_from_csv('patient_consent.csv')

if __name__ == "__main__":
    main()
