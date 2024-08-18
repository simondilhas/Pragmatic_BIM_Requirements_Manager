import os
import shutil
import pandas as pd
import streamlit as st
import uuid


# Assuming 'data' is at the same level as 'pages'
data_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'data'))

# Debug: Print the resolved absolute path to the 'data' directory
st.write(f"Resolved data directory path: {data_folder}")

# Ensure the 'data' directory exists
if not os.path.exists(data_folder):
    try:
        os.makedirs(data_folder)
    except OSError as e:
        st.error(f"Failed to create 'data' directory: {e}")
        st.stop()

def list_folders(directory):
    """List all folders in the given directory."""
    try:
        return [f for f in os.listdir(directory) if os.path.isdir(os.path.join(directory, f))]
    except Exception as e:
        st.error(f"Failed to list folders in the directory '{directory}': {e}")
        return []

def select_version_or_create_new():
    """Prompt the user to select a version or create a new one using Streamlit."""
    folders = list_folders(data_folder)
    if not folders:
        st.warning("No folders found. You might need to create a new version.")

    folders.append("Create a New Version")

    # Generate a unique key for this selectbox widget
    selectbox_key = f"version_selector_{uuid.uuid4()}"
    choice = st.selectbox("Select a version or create a new one:", folders, key=selectbox_key)

    if choice == "Create a New Version":
        # Generate a unique key for the text input widget
        text_input_key = f"new_folder_name_input_{uuid.uuid4()}"
        new_folder_name = st.text_input("Enter the name for the new version (folder):", key=text_input_key)
        if new_folder_name:
            try:
                new_folder_path = os.path.join(data_folder, new_folder_name)
                os.makedirs(new_folder_path, exist_ok=True)
                st.success(f"Created new folder: {new_folder_name}")
                return new_folder_path
            except Exception as e:
                st.error(f"Failed to create new folder '{new_folder_name}': {e}")
                return None
    else:
        return os.path.join(data_folder, choice)



def check_attributes_columns(file_path):
    """Check if the Attributes file contains the required columns."""
    required_columns = ['Column1', 'Column2', 'Column3']  # Replace with your actual column names

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

def upload_and_rename_files(version_folder):
    """Upload files and rename them to a standardized name."""
    files = {
        "Attributes": input("Upload Attributes file (enter file path): "),
        "Elements": input("Upload Elements file (enter file path): "),
        "Models": input("Upload Models file (enter file path): "),
        "Workflows": input("Upload Workflows file (enter file path): ")
    }

    standard_names = {
        "Attributes": "attributes.csv" if files["Attributes"].endswith('.csv') else "attributes.xlsx",
        "Elements": "elements.csv" if files["Elements"].endswith('.csv') else "elements.xlsx",
        "Models": "models.csv" if files["Models"].endswith('.csv') else "models.xlsx",
        "Workflows": "workflows.csv" if files["Workflows"].endswith('.csv') else "workflows.xlsx"
    }

    for key, file_path in files.items():
        if file_path:
            destination_path = os.path.join(version_folder, standard_names[key])

            if key == "Attributes":
                # Check columns in the Attributes file
                if not check_attributes_columns(file_path):
                    print(f"Skipping upload of {file_path} due to missing required columns.")
                    continue

            if os.path.exists(destination_path):
                overwrite = input(f"{standard_names[key]} already exists in {version_folder}. Do you want to overwrite it? (y/n): ")
                if overwrite.lower() != 'y':
                    print(f"Skipped uploading {file_path}")
                    continue
            
            shutil.copy(file_path, destination_path)
            print(f"Uploaded and renamed {file_path} to {destination_path}")

def main():
    """Main function to handle the complete process."""
    version_folder = select_version_or_create_new()
    upload_and_rename_files(version_folder)

# Example usage
main()
