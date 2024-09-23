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
VAR_PROJECT_NUMBER = config.get('PROJECT_NUMBER')
VAR_PROJECT_NAME = config.get('PROJECT_NAME')


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

def upload_field(upload_text, csv_file_name):
    """Handle file upload and save to the appropriate storage location."""
    uploaded_file = st.file_uploader(upload_text, type=["csv", "xlsx"])
    if uploaded_file is not None:
        file_content = uploaded_file.read()
        # Save the file in either local storage or Azure Blob storage
        store_file(file_content, st.session_state.folder_name, csv_file_name)
        st.success(f"File '{csv_file_name}' has been saved.")
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


def replace_project_details_string(folder_name, project_number, project_name):
    """Replace the strings defined in config with the actual project number and name"""

    df = load_file(folder_name, "M_Attributes.csv")
    df = df.replace({VAR_PROJECT_NUMBER: project_number, VAR_PROJECT_NAME: project_name}, regex=True)
    store_file(df, folder_name, "M_Attributes.csv")

def only_project_versions(projects: List) -> List:
    # Filter projects containing '-P-'. Ensure projects is always a list.
    return [project for project in (projects or []) if '-P-' in project]

def clear_session_state(session_states: List):
    for state in session_states:
        st.session_state[state]= None


def tab_upload_new_version():
    """Handle new version upload."""
    if 'folder_created' not in st.session_state:
        st.session_state.folder_created = False
    if 'folder_name' not in st.session_state:
        st.session_state.folder_name = ""
    

    # Folder creation section
    if not st.session_state.folder_name:
        folder_name = st.text_input("Enter the Master Template Version name/Number e.g. V2.1 :")
        if st.button("Create Master Template"):
            if folder_name:
                # Assume create_folder uses the appropriate storage
                if create_storage_folder(folder_name):
                    st.success(f"Master Template Version '{folder_name}' created successfully.")
                    st.session_state.folder_created = True
                    st.session_state.folder_name = folder_name
                else:
                    st.error(f"Failed to create Master Template Version '{folder_name}'.")
    
    # File upload section
    if st.session_state.folder_created:
        col1, col2, col3, col4 = st.columns(4)
        check1 = check2 = check3 = check4 = False

        with col1:
            file_name1 = upload_field('Upload Attributes CSV/Excel', 'M_Attributes.csv')
            if file_name1 is not None:
                check1 = check_files(st.session_state.folder_name, file_name1, required_attributes_columns)

        with col2:
            file_name2 = upload_field('Upload Elements CSV/Excel', 'M_Elements.csv')
            if file_name2 is not None:
                check2 = check_files(st.session_state.folder_name, file_name2, required_elements_columns)

        with col3:
            file_name3 = upload_field('Upload Models CSV/Excel', 'M_Models.csv')
            if file_name3 is not None:
                check3 = check_files(st.session_state.folder_name, file_name3, required_models_columns)

        with col4:
            file_name4 = upload_field('Upload Workflows CSV/Excel', 'M_Workflows.csv')
            if file_name4 is not None:
                check4 = check_files(st.session_state.folder_name, file_name4, required_workflows_columns)

        # Check if all files are uploaded and valid
        all_files_valid = check1 and check2 and check3 and check4

        # Display the button only if all files are valid
        if all_files_valid:
            if st.button("Process files and create version"):
                batch_processing_import(st.session_state.folder_name, "M")
                st.success(f"New Version {st.session_state.folder_name} is now online")
                # TODO After Uploading a Master Template, click a button to create a new one (It's not enough to clear the session states. The upload fields must be cleared aswell)
                #if st.button("Create new Master Template"):
                clear_session_state(['folder_name', 'folder_created'])
                st.rerun()
        else:
            st.warning("Please upload and validate all required files before proceeding.")


def tab_create_project():

    if 'project_created' not in st.session_state:
        st.session_state.project_created = False
    if 'project_version' not in st.session_state:
        st.session_state.project_version = None
    if 'project_language' not in st.session_state:
        st.session_state.project_language = None

    DATA_FOLDER = 'data'
    data_folder = get_project_path(DATA_FOLDER)
    available_version = get_versions(data_folder) or []


    if len(available_version) == 0:
            st.write("Create a Master Template Version first")
            
    else:
        # Step 1: Create Project Version
        if not st.session_state.project_created:
            col1, col2, col3 = st.columns(3)
            with col1:
                selected_master_template = st.selectbox("Select the Master Template Version:", available_version)
            with col2:
                project_number = st.text_input("Define the Project Number for this version: e.g. 007:")
            with col3:
                project_name = st.text_input("Define the Project Name for this version: e.g. Campus XY:")

            project_version = f"{selected_master_template}-P-{project_number}"

            if selected_master_template and project_number and project_name:
                if st.button("Create Project Version"):
                    copy_base_files(selected_master_template, project_version)
                    st.session_state.project_created = True
                    st.session_state.project_version = project_version
                    st.success(f"Project {project_version} created successfully")
                    st.rerun()
        else:
            st.success(f"Project {st.session_state.project_version} created successfully")

            # Step 2: Select Workflows
            st.write("### Select the project relevant Workflows/Usecases")
            if st.session_state.project_created:

                col1, col2, col3 = st.columns([3,3,3])

                with col1:
                    data = load_file(st.session_state.project_version, "M_Attributes.csv")
                    language_options = get_language_options(data)
                    project_language = st.selectbox("Select the Project Language:", language_options['ShortName'])
                    st.session_state.project_language = project_language

                with col2:
                    selection_option = st.selectbox(
                        "Bulk Selection",
                        options=["No Change", "Select All", "Deselect All"],
                        index=0
                    )
                with col3:
                    pass


                workflows_df = load_file(st.session_state.project_version, f"M_Workflows.csv")
                
                #if len(st.session_state.workflow_selections) == 0:
                #    st.session_state.workflow_selections = {row['WorkflowID']: row['Selected'] for _, row in workflows_df.iterrows()}

                workflows_sel = display_workflow_with_checkboxes(workflows_df, selection_option, st.session_state.project_language)

                st.info("Please note that projects cannot be edited. To make changes, you'll need to create a new version.")

                if st.button('Update Project Configuration'):
                    #try:
                    filtered_df = workflows_sel[workflows_sel['Selected'] == True]
                    st.write(filtered_df)
                    store_file(filtered_df.to_csv(index=False), st.session_state.project_version, f"M_Workflows.csv")
                    batch_processing_import(st.session_state.project_version, "P")
                    st.success(f"Project {st.session_state.project_version} configuration updated successfully")
                    st.session_state.project_created = False
                    st.session_state.project_version = None
                    #st.session_state.workflow_selections = {}
                    #st.rerun()
                    #except:
                    #    st.error(f"Error when updating Project: {st.session_state.project_version}")


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

    col_workflow_name = f"WorkflowName{language}"
    col_workflow_description = f"WorkflowDescription{language}"

    for index, row in df.iterrows():
        col1, col2, col3, col4 = st.columns([1, 2, 3, 6])
        with col1:
            checked = st.checkbox("", value=row['Selected'], key=f"checkbox_{index}")
            df.at[index, 'Selected'] = checked
        
        with col2:
            st.markdown(f"**{row['WorkflowID']}**")

        with col3:
            st.markdown(f"**{row[f'WorkflowName{language}']}**")

        with col3:
            st.markdown(row[f'WorkflowDescription{language}'])
        #st.markdown("---")

    return df

# Streamlit callback to handle checkbox changes
def checkbox_change_callback():
    st.session_state.widget_callback_called = True


            
        


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
