"""
import_csv.py

This script processes and prepares CSV data from Workflows, Models, Elements, 
and Attributes for further use.

The processed data is combined and exported as a 
comprehensive Excel file containing all the Element Plan data.

Key Features:
-------------
- Reads CSV files related to workflows, models, elements, and attributes.
- Merges the data into a single dataset.
- Exports the final dataset to a structured Excel file for further analysis or reporting.

Output:
-------
- A consolidated Excel file containing all relevant Element Plan data, 
ready for further use in analysis or reporting.

"""

import pandas as pd
from pathlib import Path
import shutil
from typing import Dict, List
import os
import sys
from dotenv import load_dotenv
import io
from io import StringIO
from datetime import datetime
import streamlit as st
 
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.load_data import load_file, store_file  # Import from load_file.py
from src.check_imports_data_structure import (
    required_workflows_columns,
    required_models_columns,
    required_elements_columns,
    required_attributes_columns,
    check_required_columns,
)

def _filter_to_selected_workflows(df):
    #Experimental!
    result_df =  df[df['Selected'] == True]
    result_df['ID'] = result_df['AttributeID'] + result_df['ModelID']
    result_df = result_df.drop_duplicates(subset=['ID']).reset_index(drop=True)
    return result_df

def _process_attributes_df(df: pd.DataFrame) -> pd.DataFrame:
    required_columns = ['ElementID', 'ModelID', 'WorkflowID', 'SortAttribute']
    check_required_columns(df, required_columns)

    #columns_to_explode = ['ElementID', 'ModelID']
    #---Test comment out for a working solution
    columns_to_explode = ['ElementID', 'ModelID', 'WorkflowID']
    
    df_exploded = df.copy()
    for column in columns_to_explode:
        # Convert column to string type
        df_exploded[column] = df_exploded[column].astype(str)
        if df_exploded[column].str.contains(',', na=False).any():
            df_exploded = df_exploded.assign(**{column: df_exploded[column].str.split(',')}).explode(column)
        df_exploded[column] = df_exploded[column].str.strip()
    
    df_exploded['SortAttribute'] = pd.to_numeric(df_exploded['SortAttribute'], errors='coerce')
    return df_exploded.sort_values('SortAttribute', na_position='last').reset_index(drop=True)

def load_file_and_add_colums(version:str, file_name:str,  column:str) -> pd.DataFrame:
    df = load_file(version, file_name)
    df[column] = True
    store_file(df.to_csv(index=False), version, file_name)
    print(f"Workflows: ------------ {df}")
    return df

def import_csv(version:str, master_or_project:str):
    """
    creates either the Master or the Project Data: Switch is "P", "M"
    """

    #Switches depending on the Flow
    if master_or_project == 'M':
        #st.write(f"Executing Master Template: {version}")

        #filename_raw_data= f"{master_or_project}_RawData"
        file_workflows = f"{master_or_project}_Workflows.csv"
        file_models = f"{master_or_project}_Models.csv"
        file_elements = f"{master_or_project}_Elements.csv"
        file_attributes = f"{master_or_project}_Attributes.csv"
        
        workflows_df = load_file_and_add_colums(version, file_workflows, 'Selected') #First Import every row is selected
        models_df = load_file(version, file_models)
        elements_df = load_file(version, file_elements)
        attributes_df = load_file(version, file_attributes)

        #Implement the logic for languages (keep all Languages)
        #languages =
   
    elif master_or_project == 'P':
        #st.write(f"Executing Project Version: {version}")
        #filename_raw_data= f"{master_or_project}_RawData"

        #Load the original files to save a project version
        file_workflows = f"M_Workflows.csv"
        file_models = f"M_Models.csv"
        file_elements = f"M_Elements.csv"
        file_attributes = f"M_Attributes.csv"

        workflows_df = load_file(version, file_workflows)
        models_df = load_file(version, file_models)
        elements_df = load_file(version, file_elements)
        attributes_df = load_file(version, file_attributes) 

        #store_file(workflows_df.to_csv(index=False),version,f"P_Workflows.csv")
        #store_file(models_df.to_csv(index=False),version,f"P_Models.csv")
        #store_file(elements_df.to_csv(index=False),version,f"P_Elements.csv")
        #store_file(attributes_df.to_csv(index=False),version,f"P_Attributes.csv")
#
    #    #Implement the logic for languages (keep all Languages)
        #languages =

    #elif master_or_project == 'P':
    #    #st.write(f"Executing Project Version: {version}")
    #    #filename_raw_data= f"{master_or_project}_RawData"
#
    #    #Load the original files to save a project version
    #    file_workflows = f"M_Workflows.csv"
    #    file_models = f"M_Models.csv"
    #    file_elements = f"M_Elements.csv"
    #    file_attributes = f"M_Attributes.csv"
#
    #    workflows_df = load_file(version, file_workflows)
    #    models_df = load_file(version, file_models)
    #    elements_df = load_file(version, file_elements)
    #    attributes_df = load_file(version, file_attributes) 
#
    #    store_file(workflows_df.to_csv(index=False),version,f"P_Workflows.csv")
    #    store_file(models_df.to_csv(index=False),version,f"P_Models.csv")
    #    store_file(elements_df.to_csv(index=False),version,f"P_Elements.csv")
    #    store_file(attributes_df.to_csv(index=False),version,f"P_Attributes.csv")
#
    #    #Implement the logic for languages (keep all Languages)
    #    #languages =
#
    #elif master_or_project == 'U':
    #    #st.write(f"Executing Update: {version}")
    #    #filename_raw_data= f"{master_or_project}_RawData"
#
    #    file_workflows = f"U_Workflows.csv" #The only file that gets updated. It's saved in 2_admin and later saved to document the changes
    #    workflows_df = load_file(version, file_workflows)
    #    store_file(workflows_df.to_csv(index=False),version,f"U{datetime.now()}_Workflows.csv")
#
    #    file_models = f"P_Models.csv"
    #    file_elements = f"P_Elements.csv"
    #    file_attributes = f"P_Attributes.csv"
#
    #    
#
    #    models_df = load_file(version, file_models)
    #    elements_df = load_file(version, file_elements)
    #    attributes_df = load_file(version, file_attributes)
#
    #    store_file(workflows_df.to_csv(index=False),version,f"U{datetime.now()}_Workflows.csv")
#
        #Implement the logic for languages (delete the columns of the unnecesssary languages)
        #languages =

    #Execution logic
    attributes_df = _process_attributes_df(attributes_df)
    merged_df = attributes_df.merge(elements_df, on='ElementID', how='left') \
                                 .merge(models_df, on='ModelID', how='left') \
                                 .merge(workflows_df, on='WorkflowID', how='left')
    
    #---test comment out for a working solutiom
    #merged_df =  merged_df[merged_df['Selected'] == True]
    merged_df = _filter_to_selected_workflows(merged_df)

    columns_to_check = ['SortModels', 'SortElements', 'SortAttributes']
    available_columns = [col for col in columns_to_check if col in merged_df.columns]

    #if available_columns:
    #    result_df = result_df.sort_values(by=available_columns, ascending=True)

    sorted_df = merged_df.sort_values(by=available_columns, ascending=[True] * len(available_columns))
    #sorted_df = sorted_df.drop_duplicates().reset_index(drop=True)

    #result_df = sorted_df.drop_duplicates().reset_index(drop=True)

    try:
        excel_buffer = io.BytesIO()
        with pd.ExcelWriter(excel_buffer, engine='openpyxl') as writer:
            #result_df.to_excel(writer, index=False)
            sorted_df.to_excel(writer, index=False)
        excel_buffer.seek(0)

        filename = f"RawData_{version}.xlsx"

        store_file(excel_buffer.getvalue(), version, filename)

    except Exception as e:
        raise ValueError(f"Error exporting DataFrame to Excel: {e}")