import os
import sys
from pathlib import Path

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.import_csv import import_csv
from src.create_formated_excel_export import create_formated_excel_export
from src.create_libal_import_file import create_libal_import_file



VERSION = 'test1'


def execute_scripts(version):
    # Add the parent directory to sys.path
    current_dir = Path(__file__).parent
    parent_dir = current_dir.parent
    sys.path.append(str(parent_dir))

    # Set the VERSION environment variable
    os.environ['VERSION'] = version

    # Execute import_csv.py
    print("Executing import_csv.py...")
    import_csv()

    # Execute create_formated_excel_export.py
    print("Executing create_formated_excel_export.py...")
    create_formated_excel_export()

    # Execute create_libal_import_file.py
    print("Executing create_libal_import_file.py...")
    create_libal_import_file()

    print("All scripts executed successfully.")

if __name__ == "__main__":
    execute_scripts(VERSION)