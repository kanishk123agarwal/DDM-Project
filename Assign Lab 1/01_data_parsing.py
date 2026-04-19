import csv
import json
import xml.etree.ElementTree as ET
import re
import os 
from html.parser import HTMLParser

# --- Helper to create dummy files if they don't exist ---
def create_dummy_files():
    if not os.path.exists('sample.txt'):
        with open('sample.txt', 'w') as f:
            f.write("This is a sample text file.\nIt has multiple lines.\nEnd of file.")
    
    if not os.path.exists('sample.html'):
        with open('sample.html', 'w') as f:
            f.write("<html><head><title>Sample</title></head><body><h1>Main Header</h1><p>Some paragraph text.</p></body></html>")
            
    if not os.path.exists('sample.xml'):
        with open('sample.xml', 'w') as f:
            f.write("<root><person><name>Alice</name><age>30</age></person><person><name>Bob</name><age>25</age></person></root>")
            
    if not os.path.exists('sample.json'):
        with open('sample.json', 'w') as f:
            f.write('[{"name": "Alice", "city": "New York"}, {"name": "Bob", "city": "Los Angeles"}]')

# --- Parsing Functions ---

def parse_text(filepath):
    print(f"--- Parsing Text File: {filepath} ---")
    try:
        with open(filepath, 'r') as f:
            content = f.read()
            print(f"Line count: {len(content.splitlines())}")
            print(f"Content snippet: {content[:50]}...")
    except Exception as e:
        print(f"Error reading text file: {e}")

def parse_csv(filepath):
    print(f"\n--- Parsing CSV File: {filepath} ---")
    data = []
    try:
        with open(filepath, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                data.append(row)
        print(f"Total records: {len(data)}")
        if data:
            print(f"Columns: {list(data[0].keys())}")
        return data
    except Exception as e:
        print(f"Error reading CSV file: {e}")
        return []

class MyHTMLParser(HTMLParser):
    def handle_starttag(self, tag, attrs):
        print(f"Start tag: {tag}")
    def handle_data(self, data):
        if data.strip():
            print(f"Data: {data.strip()}")

def parse_html(filepath):
    print(f"\n--- Parsing HTML File: {filepath} ---")
    try:
        parser = MyHTMLParser()
        with open(filepath, 'r') as f:
            parser.feed(f.read())
    except Exception as e:
        print(f"Error reading HTML file: {e}")

def parse_xml(filepath):
    print(f"\n--- Parsing XML File: {filepath} ---")
    try:
        tree = ET.parse(filepath)
        root = tree.getroot()
        for person in root.findall('person'):
            name = person.find('name').text
            age = person.find('age').text
            print(f"Person: {name}, Age: {age}")
    except Exception as e:
        print(f"Error reading XML file: {e}")

def parse_json(filepath):
    print(f"\n--- Parsing JSON File: {filepath} ---")
    try:
        with open(filepath, 'r') as f:
            data = json.load(f)
            print(f"JSON Data: {data}")
    except Exception as e:
        print(f"Error reading JSON file: {e}")

def check_anomalies(data):
    print(f"\n--- Checking Anomalies in CSV Data ---")
    missing_count = 0
    for i, row in enumerate(data):
        for key, value in row.items():
            if not value or value.strip() == "":
                print(f"Anomaly: Missing value in row {i+2} column '{key}'")
                missing_count += 1
    
    if missing_count == 0:
        print("No missing values found.")
    else:
        print(f"Total missing values found: {missing_count}")

def main():
    create_dummy_files()
    
    parse_text('sample.txt')
    
    csv_data = parse_csv('patient_consent.csv')
    if csv_data:
        check_anomalies(csv_data)
        
    parse_html('sample.html')
    parse_xml('sample.xml')
    parse_json('sample.json')

if __name__ == "__main__":
    main()
