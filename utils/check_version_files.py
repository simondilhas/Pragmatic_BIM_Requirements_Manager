import os
import pandas as pd

required_attributes_columns = [
    
]

def check_attributes_columns(file_path: str, required_columns: list):
    """Check if the Attributes file contains the required columns."""

    print(f"Checking columns in {file_path}...")

    # Check if the file exists
    if not os.path.exists(file_path):
        print(f"Error: The file {file_path} does not exist.")
        return False

    try:
        # Attempt to load the file
        if file_path.endswith('.csv'):
            df = pd.read_csv(file_path)
        elif file_path.endswith('.xlsx'):
            df = pd.read_excel(file_path)
        else:
            print(f"Unsupported file format: {file_path}")
            return False

        # Check for required columns
        if all(column in df.columns for column in required_columns):
            print("All required columns are present in the Attributes file.")
            return True
        else:
            print(f"The Attributes file is missing some required columns. Found columns: {df.columns.tolist()}")
            return False
    except Exception as e:
        print(f"An error occurred while checking the Attributes file: {e}")
        return False