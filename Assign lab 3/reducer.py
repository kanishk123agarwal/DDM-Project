import sys

def reduce_function():
    current_category = None
    total_consents = 0
    total_records = 0
    
    for line in sys.stdin:
        line = line.strip()
        
        # Ensure correct formatting
        try:
            category, flag, count = line.split('\t')
            flag = int(flag)
            count = int(count)
        except ValueError:
            continue
            
        # If we are starting a new category (because Hadoop sorts keys before passing to reducer)
        if current_category and current_category != category:
            # Emit results for the finished category
            print(f"{current_category}\tConsents: {total_consents} / Total Requests: {total_records}")
            
            # Reset counters
            total_consents = 0
            total_records = 0
            
        current_category = category
        total_consents += flag
        total_records += count
        
    # Output the last category
    if current_category:
        print(f"{current_category}\tConsents: {total_consents} / Total Requests: {total_records}")

if __name__ == "__main__":
    reduce_function()
