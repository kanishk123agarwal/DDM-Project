import re

def regex_operations():
    print("--- Regular Expression Operations ---")
    
    text = "Contact us at support@example.com or sales@example.org. Call 555-0199 for details."
    print(f"Original Text: {text}")
    
    # 1. Search (Find emails)
    print("\n1. Searching for emails:")
    email_pattern = r'[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}'
    emails = re.findall(email_pattern, text)
    print(f"Found emails: {emails}")
    
    # 2. Split (Split by punctuation)
    print("\n2. Splitting by punctuation:")
    split_text = re.split(r'[.!?]\s*', text)
    print(f"Split text: {split_text}")
    
    # 3. Replace (Redact phone numbers)
    print("\n3. Replacing phone numbers:")
    phone_pattern = r'\d{3}-\d{4}'
    redacted_text = re.sub(phone_pattern, '[REDACTED]', text)
    print(f"Redacted Text: {redacted_text}")

def main():
    regex_operations()

if __name__ == "__main__":
    main()
