import pandas as pd

def get_data_path(folder_name: str) -> Path:
    if os.getenv('STREAMLIT_CLOUD'):
        # Use a path relative to the root of the repository
        return Path('/mount/src/pragmatic_bim_requirements_manager') / folder_name
    else:
        # For local development, use the current method
        return Path(__file__).parent.parent / folder_name

df = pd.read_excel(file_name_attributes)
