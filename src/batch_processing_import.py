import os
import sys
from pathlib import Path
from io import StringIO

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.import_csv import import_csv
from src.create_formated_excel_export import create_formated_excel_export
from src.create_libal_import_file import create_libal_import_file
from src.create_data_for_web import create_data_for_web


VERSION = 'abstractBIM_V1'
master_or_project = 'M' #Master = 'M', Project Version = 'P', Update from Project = "U"



def batch_processing_import(version:str, master_or_project:str):
    """
    Executes scripts based on the provided version and type.

    Parameters:
    version (str): The version of the script or project.
    master_or_project (str): Specifies whether to run the script for "Master" or "Project".
                             Acceptable values are:
                             - "M" for Master
                             - "P" for Project
    
    Returns:
    Files in the Version folder
    """
    # Add the parent directory to sys.path
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    sys.path.append(str(parent_dir))

    # Set the VERSION environment variable
    os.environ['VERSION'] = version

    # Execute import_csv.py
    print("Executing import_csv.py...")
    import_csv(version, master_or_project)

    # Execute create_formated_excel_export.py
    print("Executing create_formated_excel_export.py...")
    create_formated_excel_export(version, master_or_project)

    # Execute create_libal_import_file.py
    print("Executing create_libal_import_file.py...")
    create_libal_import_file(version, master_or_project)

    print("Executing create_data_for_web.py...")

    create_data_for_web(version)

    print("All scripts executed successfully.")



if __name__ == "__main__":
    batch_processing_import(VERSION, master_or_project)