import streamlit as st
import hashlib
import os
import sys
import base64
import pandas as pd
from pathlib import Path

from src.batch_processing_import import execute_scripts
from src.check_imports_data_structure import (
    required_workflows_columns,
    required_models_columns,
    required_elements_columns,
    required_attributes_columns,
    check_required_columns,
)

from src.batch_processing_import import execute_scripts as execute_data_processing_scripts

# Constants for PBKDF2
SALT_LENGTH = 32
ITERATIONS = 100000
KEY_LENGTH = 32

def hash_password(password, salt=None):
    if salt is None:
        salt = os.urandom(SALT_LENGTH)
    key = hashlib.pbkdf2_hmac('sha256', password.encode(), salt, ITERATIONS, dklen=KEY_LENGTH)
    return salt + key

def verify_password(stored_password, provided_password):
    salt = stored_password[:SALT_LENGTH]
    stored_key = stored_password[SALT_LENGTH:]
    provided_key = hashlib.pbkdf2_hmac('sha256', provided_password.encode(), salt, ITERATIONS, dklen=KEY_LENGTH)
    return stored_key == provided_key

def check_password():

    def password_entered():
        stored_password = base64.b64decode(st.secrets["hashed_password"])
        if verify_password(stored_password, st.session_state["password"]):
            st.session_state["password_correct"] = True
            del st.session_state["password"]  # Don't store the password.
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        password_placeholder = st.empty()
        password_placeholder.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        return False
    
    elif not st.session_state["password_correct"]:
        password_placeholder = st.empty()
        password_placeholder.text_input(
            "Password", type="password", on_change=password_entered, key="password"
        )
        st.error("😕 Password incorrect")
        return False
    
    # Password correct.
    else:
        return True
    
def clear_session_state():
    for key in list(st.session_state.keys()):
        del st.session_state[key]
    st.success("Session state cleared!")

def logout_button():
    if st.sidebar.button("Logout"):
        clear_session_state()
        st.switch_page('pages/1_requirements.py')

def get_root_directory():
    return Path(__file__).parent.parent  # Go up one level from /pages to root

def get_data_directory():
    return get_root_directory() / "data"

def folder_exists(folder_name):
    data_dir = get_data_directory()
    return (data_dir / folder_name).exists()

def create_folder(folder_name):
    data_dir = get_data_directory()
    new_folder_path = data_dir / folder_name
    new_folder_path.mkdir(parents=True, exist_ok=True)
    return new_folder_path


def save_uploaded_file(uploaded_file, folder_name, new_file_name):
    data_dir = get_data_directory()
    folder_path = data_dir / folder_name
    folder_path.mkdir(parents=True, exist_ok=True)
    #new_file_name = "Attributes-ExportAll.csv"
    
    # Create the full file path with the new name
    file_path = folder_path / new_file_name
    
    # Write the file
    file_path.write_bytes(uploaded_file.getbuffer())
    
    return str(file_path)

def check_files(file_path, required_workflows_columns):
    df = pd.read_csv(file_path)
    message = check_required_columns(df, required_workflows_columns)
    if message is not None:
        st.write(message)
    else:
        st.write('All necessary columns exist')
        return('True')

def display_csv_preview(file_path):
    df = pd.read_csv(file_path)
    st.write(df.head())

def upload_field(upload_text ,csv_file_name):
    #st.write(f"Uploading to folder: {st.session_state.folder_name}")
    uploaded_file = st.file_uploader(upload_text, type="csv")
    if uploaded_file is not None:
        file_path = save_uploaded_file(uploaded_file, st.session_state.folder_name, csv_file_name)
        st.success(f"File has been saved'")
        #display_csv_preview(file_path)
        return(file_path)

def upload_new_version():
    if 'folder_created' not in st.session_state:
        st.session_state.folder_created = False
    if 'folder_name' not in st.session_state:
        st.session_state.folder_name = ""

    # Folder creation section
    if not st.session_state.folder_created:
        folder_name = st.text_input("Enter the Version name:")
        if st.button("Create Folder"):
            if folder_name:
                if folder_exists(folder_name):
                    st.error(f"The folder '{folder_name}' already exists. Please choose a different name.")
                else:
                    new_folder_path = create_folder(folder_name)
                    st.success(f"Folder '{folder_name}' created successfully.")
                    st.session_state.folder_created = True
                    st.session_state.folder_name = folder_name

    # File upload section
    if st.session_state.folder_created:
        col1, col2, col3, col4 = st.columns(4)
        check1 = check2 = check3 = check4 = False

        with col1:
            file_path1 = upload_field('Upload Attributes csv','Attributes-ExportAll.csv')
            if file_path1 is not None:
                check1 = check_files(file_path1, required_attributes_columns)

        with col2:
            file_path2 = upload_field('Upload Elements csv','Elements-ExportAll.csv')
            if file_path2 is not None:
                check2 = check_files(file_path2, required_elements_columns)

        with col3:
            file_path3 = upload_field('Upload Models csv','Models-ExportAll.csv')
            if file_path3 is not None:
                check3 = check_files(file_path3, required_models_columns)

        with col4:
            file_path4 = upload_field('Upload Workflows csv','Workflows-ExportAll.csv')
            if file_path4 is not None:
                check4 = check_files(file_path4, required_workflows_columns)

        # Check if all files are uploaded and valid
        all_files_valid = check1 and check2 and check3 and check4

        # Display the button only if all files are valid
        if all_files_valid:
            if st.button("Process files and create version"):
                execute_data_processing_scripts(st.session_state.folder_name)
                st.success("New Version is now online")
        else:
            st.warning("Please upload and validate all required files before proceeding.")



def main():

    if check_password():
        logout_button()
        
        # Your main app goes here
        st.title("Admin Area")

        tab1, tab2, tab3, tab4 = st.tabs(['Upload New Version', 'Compare Versions', 'Configure Version', 'Merge Version with Workflow'])

        with tab1:
            st.subheader("Upload New Version")
            upload_new_version()
            

        with tab2:
            st.subheader("Compare Versions")

        with tab3:
            st.subheader("Configure Version")

        with tab4:
            st.subheader("Merge Version with Workflow")

    else:
        with st.container():  
            st.warning("Please enter the password to access the app.")
            st.markdown("""
                        DEMO PURPOSE ONLY - NOT FOR PRODUCTION USE

To enter the admin area, use the password: "Password123!"

WARNING: This is a demonstration password. In a real application, never reveal 
passwords. For actual deployment:
1. Use a strong, unique password
2. Implement two-factor authentication (2FA)
3. Store passwords securely (hashed and salted)
4. Regularly update and rotate passwords

Remember: Security is crucial. This demo setup is not suitable for any real-world application.
                        """)

if __name__ == "__main__":
    main()