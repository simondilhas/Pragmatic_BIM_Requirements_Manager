import os
import sys
from pathlib import Path
import import_csv
import create_formated_excel_export
import create_libal_import_file

def execute_scripts(version):
    # Add the parent directory to sys.path
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    sys.path.append(str(parent_dir))

    # Set the VERSION environment variable
    os.environ['VERSION'] = version

    # Execute import_csv.py
    print("Executing import_csv.py...")
    import_csv.main()

    # Execute create_formated_excel_export.py
    print("Executing create_formated_excel_export.py...")
    create_formated_excel_export.main()

    # Execute create_libal_import_file.py
    print("Executing create_libal_import_file.py...")
    create_libal_import_file.main()

    print("All scripts executed successfully.")

if __name__ == "__main__":
    VERSION = 'SampleV.01'
    execute_scripts(VERSION)