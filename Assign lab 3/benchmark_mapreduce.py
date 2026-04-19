import os
import subprocess
import time

def run_mapreduce(csv_file, mapper_script, reducer_script, output_file):
    print(f"Running MapReduce on {csv_file}...")
    
    start_time = time.time()
    
    # Phase 1: Mapping
    with open(csv_file, "r", encoding="utf-8") as f_in:
        with open("mapped_output.txt", "w", encoding="utf-8") as f_out:
            subprocess.run(["python", mapper_script], stdin=f_in, stdout=f_out)
            
    # Phase 2: Sorting
    with open("mapped_output.txt", "r", encoding="utf-8") as f:
        lines = f.readlines()
    lines.sort()
    with open("sorted_output.txt", "w", encoding="utf-8") as f:
        f.writelines(lines)
        
    # Phase 3: Reducing
    with open("sorted_output.txt", "r", encoding="utf-8") as f_in:
        with open(output_file, "w", encoding="utf-8") as f_out:
            subprocess.run(["python", reducer_script], stdin=f_in, stdout=f_out)
            
    end_time = time.time()
    time_taken = end_time - start_time
    
    print(f"--- MapReduce Complete for {csv_file} ---")
    print(f"Time Taken: {time_taken:.4f} seconds")
    
    # Cleanup temporary files
    if os.path.exists("mapped_output.txt"): os.remove("mapped_output.txt")
    if os.path.exists("sorted_output.txt"): os.remove("sorted_output.txt")
    
    return time_taken

if __name__ == "__main__":
    # Benchmark 1: Patient Consent
    t1 = run_mapreduce(
        "patient_consent.csv", 
        "mapper.py", 
        "reducer.py", 
        "final_output_consent.txt"
    )
    
    # Benchmark 2: Healthcare Dataset
    t2 = run_mapreduce(
        "healthcare_dataset.csv", 
        "mapper_healthcare.py", 
        "reducer.py", 
        "final_output_healthcare.txt"
    )
    
    print("\n--- Summary ---")
    print(f"Patient Consent (18 rows): {t1:.4f} sec")
    print(f"Healthcare Data (~55,500 rows): {t2:.4f} sec")
