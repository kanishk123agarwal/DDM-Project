import sys

def map_function():
    for line in sys.stdin:
        line = line.strip()
        
        # Skip empty lines or header
        if not line or line.startswith('Name,Age'):
            continue
            
        fields = line.split(',')
        
        # Ensure we have the minimum expected columns (Medical Condition is at index 4)
        if len(fields) > 4:
            condition = fields[4].strip()
            if condition:
                # Emit key-value pair: condition \t 1 \t 1
                # Output format: key(category) \t flag(1) \t count(1) 
                # Our reducer expects: category \t flag \t count
                # Since we just want to count occurrences, we do count=1.
                # The reducer calculates: total_consents += flag, total_records += count
                # To make output "Consents: <x> / Total Requests: <y>" make sense, 
                # we'll just set both to 1 so the reducer handles it, or we treat flag as the condition's count.
                print(f"{condition}\t1\t1")

if __name__ == "__main__":
    map_function()
