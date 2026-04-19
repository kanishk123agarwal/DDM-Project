import sqlite3
import csv
import os

DB_NAME = 'medical_study.db'

def create_connection():
    try:
        conn = sqlite3.connect(DB_NAME)
        return conn
    except sqlite3.Error as e:
        print(f"Error connecting to database: {e}")
        return None

def create_table(conn):
    try:
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patient_id INTEGER PRIMARY KEY,
                study_id INTEGER,
                timestamp TEXT,
                demographics INTEGER,
                mental_health INTEGER
            )
        ''')
        print("Table 'patients' created successfully.")
    except sqlite3.Error as e:
        print(f"Error creating table: {e}")

def populate_db(conn, csv_file):
    print(f"Populating database from {csv_file}...")
    try:
        cursor = conn.cursor()
        with open(csv_file, 'r') as f:
            reader = csv.DictReader(f)
            count = 0
            for row in reader:
                # Insert only a subset of columns for this exercise
                cursor.execute('''
                    INSERT OR IGNORE INTO patients (patient_id, study_id, timestamp, demographics, mental_health)
                    VALUES (?, ?, ?, ?, ?)
                ''', (row['patient_id'], row['study_id'], row['timestamp'], row['demographics'], row['mental_health']))
                count += 1
        conn.commit()
        print(f"Inserted {count} records.")
    except Exception as e:
        print(f"Error populating database: {e}")

def read_data(conn):
    print("\n--- Reading Data (Select * FROM patients LIMIT 5) ---")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM patients LIMIT 5")
    rows = cursor.fetchall()
    for row in rows:
        print(row)

def update_data(conn, patient_id):
    print(f"\n--- Updating Data (Set mental_health=0 for patient_id={patient_id}) ---")
    cursor = conn.cursor()
    cursor.execute("UPDATE patients SET mental_health = 0 WHERE patient_id = ?", (patient_id,))
    conn.commit()
    print("Update complete.")
    
    # Verify
    cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    print(f"Updated Record: {cursor.fetchone()}")

def delete_data(conn, patient_id):
    print(f"\n--- Deleting Data (patient_id={patient_id}) ---")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM patients WHERE patient_id = ?", (patient_id,))
    conn.commit()
    print("Delete complete.")
    
    # Verify
    cursor.execute("SELECT * FROM patients WHERE patient_id = ?", (patient_id,))
    result = cursor.fetchone()
    if result is None:
        print("Record successfully deleted.")
    else:
        print("Record still exists.")

def main():
    if os.path.exists(DB_NAME):
        os.remove(DB_NAME) # Clean start
        
    conn = create_connection()
    if conn:
        create_table(conn)
        populate_db(conn, 'patient_consent.csv')
        read_data(conn)
        
        # CRUD Operations
        update_data(conn, 1001)
        delete_data(conn, 1002)
        
        conn.close()

if __name__ == "__main__":
    main()
