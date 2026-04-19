import sys

# Define the category names based on the CSV structure
CATEGORIES = [
    "demographics",
    "mental_health",
    "biospecimen",
    "family_history",
    "genetic",
    "clinical_info",
    "sexual_reproductive"
]

def map_function():
    for line in sys.stdin:
        # Remove leading/trailing whitespace
        line = line.strip()
        
        # Skip empty lines or header
        if not line or line.startswith('patient_id'):
            continue
            
        # Split line by comma
        fields = line.split(',')
        
        # Ensure we have all 10 columns
        if len(fields) != 10:
            continue
            
        # Extract the consent flags (columns 3 to 9)
        consent_flags = fields[3:10]
        
        # Iterate over each category and its corresponding flag
        for category, flag in zip(CATEGORIES, consent_flags):
            try:
                # Validate the flag is '0' or '1'
                if flag in ['0', '1']:
                    # Emit key-value pair: category \t flag
                    # We output the count of records as well, so we can calculate total consents and total records
                    print(f"{category}\t{flag}\t1")
            except ValueError:
                pass

if __name__ == "__main__":
    map_function()
