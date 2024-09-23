import streamlit as st
import os
import io
import pandas as pd
import time
from typing import List
from dotenv import load_dotenv
from st_aggrid import AgGrid, GridOptionsBuilder,GridUpdateMode
from st_aggrid.grid_options_builder import GridOptionsBuilder

from src.load_data import load_file, store_file, create_storage_folder # Assuming load_file is imported here
from src.check_imports_data_structure import (
    required_workflows_columns,
    required_models_columns,
    required_elements_columns,
    required_attributes_columns,
    check_required_columns,
)

from src.batch_processing_import import batch_processing_import
from src.password_utils import check_password, logout_button
from src.ui_elements import custom_sidebar  
from src.utils import load_config
from src.load_data import load_file, get_versions, get_project_path, copy_base_files



config = load_config()
MAIN_LANGUAGE = config.get('MAIN_LANGUAGE', False)
FRONTEND_LANGUAGES = config.get('FRONTEND_LANGUAGES')
VAR_PROJECT_NUMBER = config.get('VARIABLES', {}).get('PROJECT_NUMBER')
VAR_PROJECT_NAME = config.get('VARIABLES', {}).get('PROJECT_NAME')


def check_files(version_name, file_name, required_columns):
    """Load and validate the file against the required columns."""
    df = load_file(version_name, file_name)  # Load the file content

    message = check_required_columns(df, required_columns)
    if message is not None:
        st.error(message)
        return False
    else:
        st.success('All necessary columns exist')
        st.dataframe(df)
        return True

def upload_field(folder_name, upload_text, csv_file_name):
    """Handle file upload and save to the appropriate storage location."""
    uploaded_file = st.file_uploader(upload_text, type=["csv"])
    if uploaded_file is not None:
        file_content = uploaded_file.read()
        # Save the file in either local storage or Azure Blob storage
        store_file(file_content, folder_name, csv_file_name)
        #st.success(f"File '{csv_file_name}' has been saved.")
        return csv_file_name  # Return the name of the saved file

def get_available_languages(df: pd.DataFrame) -> List[str]:
    language_columns = [col for col in df.columns if col.startswith('AttributeDescription') and len(col) > len('AttributeDescription')]
    return [col[len('AttributeDescription'):] for col in language_columns]

def get_language_options(data):
    # Language code to full name mapping
    language_names = {
        'EN': 'English',
        'DE': 'Deutsch',
        'FR': 'Français',
        'IT': 'Italiano',
        # Add more languages as needed
    }

    available_languages = get_available_languages(data)
    language_options = [lang for lang in available_languages if lang in language_names]
    language_display_names = [language_names.get(lang, lang) for lang in language_options]

    result_dict = {
        'ShortName' : language_options,
        'LongName' : language_display_names
    }

    return result_dict


def x_replace_project_details_string(project_number, project_name):
    """Replace the strings defined in config with the actual project number and name"""
    df = load_file(project_number, "M_Attributes.csv")
    df = df.replace({VAR_PROJECT_NUMBER: project_number, VAR_PROJECT_NAME: project_name}, regex=True)
    store_file(df, project_number, "M_Attributes.csv")

def replace_project_details_string(project_number, project_name):
    """Replace the strings defined in config with the actual project number and name"""
    df = load_file(project_number, "M_Attributes.csv")
    
    # Create a dictionary for replacements
    replacements = {
        VAR_PROJECT_NUMBER: project_number,
        VAR_PROJECT_NAME: project_name
    }
    
    print(replacements)

    # Apply replacements to all string columns
    for column in df.select_dtypes(include=['object']):
        df[column] = df[column].replace(replacements, regex=True)
    
    store_file(df, project_number, "M_Attributes.csv")


def only_project_versions(projects: List) -> List:
    # Filter projects containing '-P-'. Ensure projects is always a list.
    return [project for project in (projects or []) if '-P-' in project]

def x_clear_session_state(session_states: List):
    for state in session_states:
        st.session_state[state]= None

import streamlit as st
from typing import List, Optional

def x_clear_session_state(keys_to_clear: Optional[List[str]] = None):
    """
    Clear specified keys from session state, or all if none specified.
    Also clear all input widgets.
    """
    if keys_to_clear is None:
        # Clear all session state
        st.session_state.clear()
    else:
        # Clear specified keys
        for key in keys_to_clear:
            if key in st.session_state:
                del st.session_state[key]
    
    # Reset all input widgets
    for key in st.session_state:
        if isinstance(st.session_state[key], (str, int, float)):
            st.session_state[key] = ""
        elif isinstance(st.session_state[key], bool):
            st.session_state[key] = False
        elif isinstance(st.session_state[key], list):
            st.session_state[key] = []

    # Rerun the app
    st.rerun()

def clear_session_state():
    """
    Aggressively clear all session state variables and reset to default values.
    """
    # List of keys to preserve (if any)
    keys_to_preserve = []

    # Clear everything except preserved keys
    for key in list(st.session_state.keys()):
        if key not in keys_to_preserve:
            del st.session_state[key]

    # Set default values
    default_values = {
        'folder_created': False,
        'project_version': None,
        'folder_name': '',
        'password_correct': False,
        'project_language': None,
        'language_suffix': None,
        'project_name': None,
        'project_created': False
    }

    # Update session state with default values
    st.session_state.update(default_values)

    # Reset all checkboxes
    for key in list(st.session_state.keys()):
        if key.startswith('checkbox_'):
            st.session_state[key] = False

    # Force a rerun of the app
    st.rerun()

def aagrid_display_workflow_with_checkboxes(df):

    st.write("### Select the project relevant Workflows/Usecases")

    # Function to update all rows
    def update_all(df, value):
        df['Selected'] = value
        return df

    # Dropdown for bulk selection
    selection_option = st.selectbox(
        "Bulk Selection",
        options=["No Change", "Select All", "Deselect All"],
        index=0
    )

    if selection_option == "Select All":
        df = update_all(df, True)
    elif selection_option == "Deselect All":
        df = update_all(df, False)

    gb = GridOptionsBuilder.from_dataframe(df)
    
    gb.configure_column("Selected", 
                        header_name="Selected", 
                        cellRenderer='agCheckboxCellRenderer',
                        cellEditor='agCheckboxCellEditor',
                        editable=True,
                        width=100)
    gb.configure_column("WorkflowID", header_name="Workflow ID")
    gb.configure_column("WorkflowNameDE", header_name="Workflow Name")
    gb.configure_column("WorkflowDescriptionDE", header_name="Description")
    
    gb.configure_grid_options(suppressRowClickSelection=True)
    gridOptions = gb.build()

    grid_response = AgGrid(
        df,
        gridOptions=gridOptions,
        data_return_mode='AS_INPUT', 
        update_mode=GridUpdateMode.VALUE_CHANGED,
        fit_columns_on_grid_load=True,
        theme='streamlit'
    )

    updated_df = grid_response['data']
    
    # Ensure 'Selected' column contains boolean values
    updated_df['Selected'] = updated_df['Selected'].astype(bool)

    return updated_df

def check_dropdown():
    selection_option = st.selectbox(
        "Bulk Selection",
        options=["No Change", "Select All", "Deselect All"],
        index=0
    )


def display_workflow_with_checkboxes(df, selection_option, language):
    #st.write("### Select the project relevant Workflows/Usecases")

    # Function to update all rows
    def update_all(df, value):
        df['Selected'] = value
        return df
    
    if selection_option == "Select All":
        df = update_all(df, True)
    elif selection_option == "Deselect All":
        df = update_all(df, False)
    #Add here more predefined Selections

    for index, row in df.iterrows():
        col1, col2, col3, col4 = st.columns([1, 2, 3, 6])
        with col1:
            checked = st.checkbox("", value=row['Selected'], key=f"checkbox_{index}")
            df.at[index, 'Selected'] = checked
        
        with col2:
            st.markdown(f"{row['WorkflowID']}")

        with col3:
            st.markdown(f"{row[f'WorkflowName{language}']}")

        with col3:
            st.markdown(row[f'WorkflowDescription{language}'])
        #st.markdown("---")

    return df



def checkbox_change_callback():
    st.session_state.widget_callback_called = True


def x_tab_upload_new_version():
    if 'project_state' not in st.session_state:
        st.session_state.project_state = {
            'folder_created': False,
            'folder_name': None,
            'master_created': False,
        }
    else:
        # Ensure all keys exist
        default_state = {
            'folder_created': False,
            'folder_name': None,
            'master_created': False
        }
        for key, value in default_state.items():
            if key not in st.session_state.project_state:
                st.session_state.project_state[key] = value

    # Always show option to reset
    if st.sidebar.button('Reset Master Creation Process'):
        st.session_state.project_state = {
            'folder_created': False,
            'folder_name': None,
            'master_created': False
        }
        st.rerun()

    # Folder creation section
    if not st.session_state.project_state.get('folder_created', False):
        folder_name = st.text_input("Enter the Master Template Version name/Number e.g. V2.1 :")
        if st.button("Create Master Template"):
            if folder_name:
                # Assume create_folder uses the appropriate storage
                if create_storage_folder(folder_name):
                    st.success(f"Master Template Version '{folder_name}' created successfully.")
                    st.session_state.project_state['folder_created'] = True
                    st.session_state.project_state['folder_name'] = folder_name
                    st.rerun()  # Rerun to update the UI
                else:
                    st.error(f"Failed to create Master Template Version '{folder_name}'.")
            else:
                st.warning("Please enter a folder name.")
    
    # File upload section
    if st.session_state.project_state.get('folder_created', False):
        col1, col2, col3, col4 = st.columns(4)
        check1 = check2 = check3 = check4 = False

        with col1:
            file_name1 = upload_field('Upload Attributes CSV', 'M_Attributes.csv')
            if file_name1 is not None:
                check1 = check_files(st.session_state.folder_name, file_name1, required_attributes_columns)

        with col2:
            file_name2 = upload_field('Upload Elements CSV', 'M_Elements.csv')
            if file_name2 is not None:
                check2 = check_files(st.session_state.folder_name, file_name2, required_elements_columns)

        with col3:
            file_name3 = upload_field('Upload Models CSV', 'M_Models.csv')
            if file_name3 is not None:
                check3 = check_files(st.session_state.folder_name, file_name3, required_models_columns)

        with col4:
            file_name4 = upload_field('Upload Workflows CSV', 'M_Workflows.csv')
            if file_name4 is not None:
                check4 = check_files(st.session_state.folder_name, file_name4, required_workflows_columns)

        # Check if all files are uploaded and valid
        all_files_valid = check1 and check2 and check3 and check4

        # Display the button only if all files are valid
        if all_files_valid:
            if st.button("Process files and create version"):
                batch_processing_import(st.session_state.folder_name, "M")
                st.success(f"New Version {st.session_state.folder_name} is now online")
                #st.session_state.master_created = True

                

                #st.session_state.project_state = {
                #    'folder_created': False,
                #    'folder_name': None,
                #}
                
        else:
            st.warning("Please upload and validate all required files before proceeding.")


def tab_upload_new_version():
    if 'project_state' not in st.session_state:
        st.session_state.project_state = {
            'folder_created': False,
            'folder_name': None,
            'master_created': False,
            'version_online': False,
        }
    else:
        # Ensure all keys exist
        default_state = {
            'folder_created': False,
            'folder_name': None,
            'master_created': False,
            'version_online': False,
        }
        for key, value in default_state.items():
            if key not in st.session_state.project_state:
                st.session_state.project_state[key] = value

    # Always show option to reset
    #if st.sidebar.button('Reset Master Creation Process'):
    #    st.session_state.project_state = {
    #        'folder_created': False,
    #        'folder_name': None,
    #        'master_created': False,
    #        'version_online': False,
    #    }
    #    st.rerun()

    # Folder creation section
    if not st.session_state.project_state.get('folder_created', False):
        folder_name = st.text_input("Enter the Master Template Version name/Number e.g. V2.1 :")
        if st.button("Create Master Template"):
            if folder_name:
                # Assume create_folder uses the appropriate storage
                if create_storage_folder(folder_name):
                    st.success(f"Master Template Version '{folder_name}' created successfully.")
                    st.session_state.project_state['folder_created'] = True
                    st.session_state.project_state['folder_name'] = folder_name
                    st.rerun()  # Rerun to update the UI
                else:
                    st.error(f"Failed to create Master Template Version '{folder_name}'.")
            else:
                st.warning("Please enter a folder name.")
    
    # File upload section
    if st.session_state.project_state.get('folder_created', False) and not st.session_state.project_state.get('version_online', False):
        col1, col2, col3, col4 = st.columns(4)
        check1 = check2 = check3 = check4 = False

        folder_name = st.session_state.project_state['folder_name']

        with col1:
            file_name1 = upload_field(folder_name, 'Upload Attributes CSV', 'M_Attributes.csv')
            if file_name1 is not None:
                try:
                    check1 = check_files(folder_name, file_name1, required_attributes_columns)
                except Exception as e:
                    st.error(f"Error checking Attributes file: {str(e)}")

        with col2:
            file_name2 = upload_field(folder_name, 'Upload Elements CSV', 'M_Elements.csv')
            if file_name2 is not None:
                try:
                    check2 = check_files(folder_name, file_name2, required_elements_columns)
                except Exception as e:
                    st.error(f"Error checking Elements file: {str(e)}")

        with col3:
            file_name3 = upload_field(folder_name, 'Upload Models CSV', 'M_Models.csv')
            if file_name3 is not None:
                try:
                    check3 = check_files(folder_name, file_name3, required_models_columns)
                except Exception as e:
                    st.error(f"Error checking Models file: {str(e)}")

        with col4:
            file_name4 = upload_field(folder_name,'Upload Workflows CSV', 'M_Workflows.csv')
            if file_name4 is not None:
                try:
                    check4 = check_files(folder_name, file_name4, required_workflows_columns)
                except Exception as e:
                    st.error(f"Error checking Workflows file: {str(e)}")

        # Check if all files are uploaded and valid
        all_files_valid = check1 and check2 and check3 and check4

        # Display the button only if all files are valid
        if all_files_valid:
            if st.button("Process files and create version"):
                try:
                    batch_processing_import(st.session_state.project_state['folder_name'], "M")
                    st.success(f"New Version {st.session_state.project_state['folder_name']} is now online")
                    st.session_state.project_state['version_online'] = True
                    
                    st.rerun()
                except Exception as e:
                    st.error(f"Error processing files: {str(e)}")
        else:
            st.warning("Please upload and validate all required files before proceeding.")

    # Option to create a new version after successful upload
    if st.session_state.project_state.get('version_online', False):
        st.success(f"Version {st.session_state.project_state['folder_name']} is online.")
        if st.button('Create a new Master Version'):
            st.session_state.project_state = {
                'folder_created': False,
                'folder_name': None,
                'master_created': False,
                'version_online': False,
            }
            st.success("Ready to create a new Master Version!")
            st.rerun()


def tab_create_project():
    # Initialize session state variables
    if 'project_state' not in st.session_state:
        st.session_state.project_state = {
            'version': "",
            'language': None,
            'name': None,
            'create_project_step': 1
        }
    else:
        # Ensure all keys exist
        default_state = {
            'version': "",
            'language': None,
            'name': None,
            'create_project_step': 1
        }
        for key, value in default_state.items():
            if key not in st.session_state.project_state:
                st.session_state.project_state[key] = value

    # Display current state (for debugging, can be removed in production)
    #st.write(st.session_state.project_state)

    DATA_FOLDER = 'data'
    data_folder = get_project_path(DATA_FOLDER)
    available_versions = get_versions(data_folder) or []

    if not available_versions:
        st.write("Create a Master Template Version first")
        return
    
    else:
        # Step 1: Create Project Version
        if st.session_state.project_state['create_project_step'] == 1:
            col1, col2, col3 = st.columns(3)
            with col1:
                selected_master_template = st.selectbox("Select the Master Template Version:", available_versions)
            with col2:
                project_number = st.text_input("Define the Project Number for this version: e.g. 007:")
            with col3:
                project_name = st.text_input("Define the Project Name for this version: e.g. Campus XY:")

            project_version = f"{selected_master_template}-P-{project_number}"

            if selected_master_template and project_number and project_name:
                if st.button("Create Project Version"):
                    copy_base_files(selected_master_template, project_version)
                    st.session_state.project_state.update({
                        'version': project_version,
                        'name': project_name,
                        'create_project_step': 2
                    })
                    st.success(f"Project {project_version} created successfully")
                    st.rerun()


        # Step 2: Select Workflows
        if st.session_state.project_state['create_project_step'] == 2:
            st.write("### Select the project relevant Workflows/Usecases")

            col1, col2, _ = st.columns([3,3,3])

            project_version = st.session_state.project_state['version']

            with col1:
                data = load_file(project_version, "M_Attributes.csv")
                language_options = get_language_options(data)
                project_language = st.selectbox("Select the Project Language:", language_options['ShortName'])
                st.session_state.project_state['language'] = project_language

            with col2:
                selection_option = st.selectbox(
                    "Bulk Selection",
                    options=["No Change", "Select All", "Deselect All"],
                    index=0
                )

            selected_project = st.session_state.project_state['version']
            project_name = st.session_state.project_state['name']

            workflows_df = load_file(selected_project, "M_Workflows.csv")
            workflows_sel = display_workflow_with_checkboxes(workflows_df, selection_option, project_language)
            
            if st.button('Update Project Configuration'):
                try:
                    filtered_df = workflows_sel[workflows_sel['Selected'] == True]
                    store_file(filtered_df.to_csv(index=False), selected_project, "M_Workflows.csv")
                    replace_project_details_string(selected_project, project_name)
                    batch_processing_import(selected_project, "P")
                    st.session_state.project_state.update({
                        'language': project_language,
                        'create_project_step': 3
                    })
                    st.rerun()
                except Exception as e:
                    st.error(f"Error when updating Project: {selected_project}. Error: {str(e)}")

        
        if st.session_state.project_state['create_project_step']  == 3:
            st.success(f"Project configuration updated successfully")
            if st.button("Create a new project"):
                st.session_state.project_state = {
                    'version': "",
                    'language': None,
                    'name': None,
                    'create_project_step': 1
                }
                st.rerun()


def main():
    custom_sidebar(MAIN_LANGUAGE)
    if check_password():
        logout_button()
        
        st.title("Admin Area")
        tab1, tab2, tab3= st.tabs(['New Masters Template', 'Create Project Version', '...' ])

        with tab1:
            st.subheader("New Masters Template")
            tab_upload_new_version()

        with tab2:
            st.subheader("Create Project Version")
            tab_create_project()
            

        with tab3:
            st.subheader("...")
    




    else:
        st.warning("Please enter the password to access the app.")
        st.markdown("""
            DEMO PURPOSE ONLY - NOT FOR PRODUCTION USE - AT LEAST CHANGE THE PASSWORD, BETTER REPLACE THE LOGIC

            To enter the admin area, use the password: "Password123"
        """)


if __name__ == "__main__":
    main()
