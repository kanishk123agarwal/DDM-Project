import csv
import sys

# Try importing pymongo
try:
    from pymongo import MongoClient, ASCENDING
    from pymongo.errors import ConnectionFailure
except ImportError:
    print("pymongo module not found. Please install it using 'pip install pymongo'.")
    sys.exit(1)

DB_NAME = 'medical_study_db'
COLLECTION_NAME = 'patients'

def get_database():
    # Provide the mongodb atlas url to connect python to mongodb using pymongo
    CONNECTION_STRING = "mongodb://localhost:27017/"
    try:
        client = MongoClient(CONNECTION_STRING, serverSelectionTimeoutMS=2000)
        # Check if the server is available
        client.admin.command('ping')
        return client[DB_NAME]
    except ConnectionFailure:
        print("MongoDB not available. Ensure the server is running on localhost:27017")
        return None

def insert_data(db, csv_file):
    print("\n--- Inserting Data from CSV ---")
    collection = db[COLLECTION_NAME]
    # Clear existing data for clean run
    collection.delete_many({})
    
    data_to_insert = []
    try:
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            for row in reader:
                # Convert numeric fields
                row['patient_id'] = int(row['patient_id'])
                row['study_id'] = int(row['study_id'])
                row['demographics'] = int(row['demographics'])
                row['mental_health'] = int(row['mental_health'])
                data_to_insert.append(row)
        
        if data_to_insert:
            result = collection.insert_many(data_to_insert)
            print(f"Inserted {len(result.inserted_ids)} documents.")
    except Exception as e:
        print(f"Error inserting data: {e}")

def search_data(db):
    print("\n--- Searching Data (Find one patient) ---")
    collection = db[COLLECTION_NAME]
    result = collection.find_one({'patient_id': 1001})
    print(f"Found: {result}")

def update_data(db):
    print("\n--- Updating Data (Set mental_health=0 for patient_id=1001) ---")
    collection = db[COLLECTION_NAME]
    result = collection.update_one({'patient_id': 1001}, {'$set': {'mental_health': 0}})
    print(f"Matched: {result.matched_count}, Modified: {result.modified_count}")

def delete_data(db):
    print("\n--- Deleting Data (patient_id=1002) ---")
    collection = db[COLLECTION_NAME]
    result = collection.delete_one({'patient_id': 1002})
    print(f"Deleted count: {result.deleted_count}")

def aggregate_data(db):
    print("\n--- Aggregating Data (Count by study_id) ---")
    collection = db[COLLECTION_NAME]
    pipeline = [
        {"$group": {"_id": "$study_id", "count": {"$sum": 1}}}
    ]
    results = collection.aggregate(pipeline)
    for doc in results:
        print(doc)

def create_index(db):
    print("\n--- Creating Index on patient_id ---")
    collection = db[COLLECTION_NAME]
    result = collection.create_index([('patient_id', ASCENDING)], unique=True)
    print(f"Index created: {result}")

def main():
    db = get_database()
    if db is not None:
        insert_data(db, 'patient_consent.csv')
        create_index(db)
        search_data(db)
        update_data(db)
        delete_data(db)
        aggregate_data(db)
    else:
        print("Skipping MongoDB operations due to connection failure.")

if __name__ == "__main__":
    main()
