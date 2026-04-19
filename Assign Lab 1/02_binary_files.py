import pickle
import struct
import os

def pickle_operations():
    print("--- Pickle Operations ---")
    data = {
        'id': 1,
        'name': 'Test User',
        'scores': [10, 20, 30],
        'active': True
    }
    filename = 'data.pickle'
    
    # Write
    print(f"Writing dictionary to {filename}...")
    try:
        with open(filename, 'wb') as f:
            pickle.dump(data, f)
        print("Write successful.")
    except Exception as e:
        print(f"Error writing pickle: {e}")
        return

    # Read
    print(f"Reading dictionary from {filename}...")
    try:
        with open(filename, 'rb') as f:
            loaded_data = pickle.load(f)
        print(f"Loaded Data: {loaded_data}")
        print(f"Data matches: {data == loaded_data}")
    except Exception as e:
        print(f"Error reading pickle: {e}")

def struct_operations():
    print("\n--- Struct Operations ---")
    filename = 'data.bin'
    
    # Data to pack: int, float, boolean (as int)
    # i = int (4 bytes), f = float (4 bytes), ? = bool (1 byte)
    val1 = 1024
    val2 = 3.14159
    val3 = True
    
    # Write
    print(f"Packing values ({val1}, {val2}, {val3}) to {filename}...")
    try:
        with open(filename, 'wb') as f:
            # Pack data
            packed_data = struct.pack('if?', val1, val2, val3)
            f.write(packed_data)
        print("Write successful.")
    except Exception as e:
        print(f"Error writing struct: {e}")
        return

    # Read
    print(f"Reading values from {filename}...")
    try:
        with open(filename, 'rb') as f:
            read_data = f.read()
            # Unpack
            unpacked_val1, unpacked_val2, unpacked_val3 = struct.unpack('if?', read_data)
        
        print(f"Unpacked Values: {unpacked_val1}, {unpacked_val2:.5f}, {unpacked_val3}")
    except Exception as e:
        print(f"Error reading struct: {e}")

def main():
    pickle_operations()
    struct_operations()

if __name__ == "__main__":
    main()
