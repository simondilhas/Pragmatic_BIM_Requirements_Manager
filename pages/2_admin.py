import streamlit as st
import os
import io
import pandas as pd
from dotenv import load_dotenv
from src.load_data import load_file, store_file, create_storage_folder # Assuming load_file is imported here
from src.check_imports_data_structure import (
    required_workflows_columns,
    required_models_columns,
    required_elements_columns,
    required_attributes_columns,
    check_required_columns,
)

from src.batch_processing_import import execute_scripts as execute_data_processing_scripts
from src.password_utils import check_password, logout_button
from src.ui_elements import custom_sidebar  
from src.utils import load_config



config = load_config()
MAIN_LANGUAGE = config.get('MAIN_LANGUAGE', False)

def check_files(version_name, file_name, required_columns):
    """Load and validate the file against the required columns."""
    df = load_file(version_name, file_name)  # Load the file content

    message = check_required_columns(df, required_columns)
    if message is not None:
        st.write(message)
        return False
    else:
        st.write('All necessary columns exist')
        st.dataframe(df)
        return True

def upload_field(upload_text, csv_file_name):
    """Handle file upload and save to the appropriate storage location."""
    uploaded_file = st.file_uploader(upload_text, type=["csv", "xlsx"])
    if uploaded_file is not None:
        file_content = uploaded_file.read()
        # Save the file in either local storage or Azure Blob storage
        store_file(file_content, st.session_state.folder_name, csv_file_name)
        st.success(f"File '{csv_file_name}' has been saved.")
        return csv_file_name  # Return the name of the saved file


def tab_upload_new_version():
    """Handle new version upload."""
    if 'folder_created' not in st.session_state:
        st.session_state.folder_created = False
    if 'folder_name' not in st.session_state:
        st.session_state.folder_name = ""

    # Folder creation section
    if not st.session_state.folder_created:
        folder_name = st.text_input("Enter the Version name:")
        if st.button("Create Folder"):
            if folder_name:
                # Assume create_folder uses the appropriate storage
                if create_storage_folder(folder_name):
                    st.success(f"Folder '{folder_name}' created successfully.")
                    st.session_state.folder_created = True
                    st.session_state.folder_name = folder_name
                else:
                    st.error(f"Failed to create folder '{folder_name}'.")
    
    # File upload section
    if st.session_state.folder_created:
        col1, col2, col3, col4 = st.columns(4)
        check1 = check2 = check3 = check4 = False

        with col1:
            file_name1 = upload_field('Upload Attributes CSV/Excel', 'Attributes-ExportAll.csv')
            if file_name1 is not None:
                check1 = check_files(st.session_state.folder_name, file_name1, required_attributes_columns)

        with col2:
            file_name2 = upload_field('Upload Elements CSV/Excel', 'Elements-ExportAll.csv')
            if file_name2 is not None:
                check2 = check_files(st.session_state.folder_name, file_name2, required_elements_columns)

        with col3:
            file_name3 = upload_field('Upload Models CSV/Excel', 'Models-ExportAll.csv')
            if file_name3 is not None:
                check3 = check_files(st.session_state.folder_name, file_name3, required_models_columns)

        with col4:
            file_name4 = upload_field('Upload Workflows CSV/Excel', 'Workflows-ExportAll.csv')
            if file_name4 is not None:
                check4 = check_files(st.session_state.folder_name, file_name4, required_workflows_columns)

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
    custom_sidebar(MAIN_LANGUAGE)

    """Main admin area function."""
    if check_password():
        logout_button()
        
        st.title("Admin Area")
        tab1, tab2, tab3, tab4 = st.tabs(['Upload New Version', 'Compare Versions', 'Configure Version', 'Merge Version with Workflow'])

        with tab1:
            st.subheader("Upload New Version")
            tab_upload_new_version()

        with tab2:
            st.subheader("Compare Versions")

        with tab3:
            st.subheader("Configure Version")

        with tab4:
            st.subheader("Merge Version with Workflow")

    else:
        st.warning("Please enter the password to access the app.")
        st.markdown("""
            DEMO PURPOSE ONLY - NOT FOR PRODUCTION USE - AT LEAST CHANGE THE PASSWORD, BETTER REPLACE THE LOGIC

            To enter the admin area, use the password: "Password123"
        """)


if __name__ == "__main__":
    main()
