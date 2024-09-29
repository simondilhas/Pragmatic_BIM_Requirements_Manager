"""
load_files.py i

This module provides an abstraction layer for loading, saving, and managing element plan data
across different storage options, such as local file storage, Azure Blob Storage, 
and potentially other cloud services / Databases.

"""

import pandas as pd
import logging
from azure.storage.blob import BlobServiceClient, generate_blob_sas, BlobSasPermissions
from azure.core.exceptions import AzureError, ResourceExistsError
from datetime import datetime, timedelta, timezone
from pathlib import Path
import os
import io
from typing import List
from src.utils import load_config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

config = load_config()

USE_AZURE_STORAGE = config.get('USE_AZURE_STORAGE', False)

AZURE_ACCOUNT_NAME = os.getenv('AZURE_ACCOUNT_NAME')
AZURE_ACCOUNT_KEY = os.getenv('AZURE_ACCOUNT_KEY')
AZURE_CONTAINER_NAME = os.getenv('AZURE_CONTAINER_NAME')




def create_storage_folder(version_name: str):
    """Creates a storage folder in either Azure or locally based on configuration."""
    if USE_AZURE_STORAGE:
        return _create_azure_directory(version_name)
    else:
        return _create_local_directory(version_name)


def store_file(file_content: str, version_name: str, file_name: str) -> pd.DataFrame:
    """Saves a file either in Azure Blob or locally based on configuration."""

    if USE_AZURE_STORAGE:
        return _upload_to_azure(file_content, version_name, file_name)
    else:
        return _store_locally(file_content, version_name, file_name)


def load_file(version_name: str, file_name: str) -> pd.DataFrame:
    """
    Loads a CSV or Excel file from Azure Blob Storage or the local filesystem based on configuration.

    Parameters:
    ----------
    version_name : str
        The name of the version or folder where the file is located.
    file_name : str
        The name of the file to be loaded (should be a CSV or Excel file).

    Returns:
    -------
    pd.DataFrame
        The contents of the file as a Pandas DataFrame.

    Raises:
    -------
    RuntimeError:
        If the file cannot be loaded from Azure Blob Storage or locally.

    Example:
    --------
    df = load_file("v1", "example.csv")
    """
    try:
        if USE_AZURE_STORAGE:
            # Attempt to load the file from Azure Blob Storage
            return _load_from_azure(version_name, file_name)
        else:
            # Load the file from the local filesystem
            return _load_locally(version_name, file_name)
    
    except Exception as e:
        raise RuntimeError(f"Failed to load file {file_name} from {version_name}: {str(e)}")

def get_versions(data_folder: Path) -> List[str]:
    """ Get a list of all the folders/versions"""
    if USE_AZURE_STORAGE:
        # Fetch versions from Azure Blob Storage
        blob_service_client = BlobServiceClient(
            account_url=f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net",
            credential=AZURE_ACCOUNT_KEY
        )
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        blobs = container_client.list_blobs()
        return sorted(
            {blob.name.split('/')[0] for blob in blobs if '__pycache__' not in blob.name},
            reverse=True
        )
    else:
        # Fetch versions from the local file system
        return sorted([f.name for f in data_folder.iterdir() 
                       if f.is_dir() and f.name != '__pycache__'], reverse=True)

def get_project_path(folder_name: str) -> Path:
    """Get the appropriate project path based on the environment (local or Streamlit Cloud)."""
    if os.getenv('STREAMLIT_CLOUD'):
        return Path('/mount/src/pragmatic_bim_requirements_manager') / folder_name
    else:
        return Path(__file__).parent.parent / folder_name
    

import os
from pathlib import Path


def copy_base_files(selected_master_template: str, project_version: str):
    """Copy all CSV files from the selected master template to the project version folder."""

    # Create the target directory in Azure or locally
    create_storage_folder(project_version)

    # Fetch files from master template folder
    if USE_AZURE_STORAGE:
        _copy_files_azure(selected_master_template, project_version)
    else:
        _copy_files_local(selected_master_template, project_version)

def get_download_link(version: str, file_name: str, data_folder: str) -> str:
    """
    Generates a file path to serve the file.

    Parameters:
    ----------
    version_name : str
        The name of the version or folder where the file is located.
    file_name : str
        The name of the file to be downloaded.
    data_folder : str
        The base folder where the local files are stored.

    Returns:
    -------
    str
        Either the local file path or the Azure Link

    """

    print("debug start get_download_link")

    if USE_AZURE_STORAGE:
            # Generate Azure download link
            download_url = _get_azure_download_link(version, file_name)
            print(download_url)
    else:
        # Generate local download link
        download_url = _get_local_download_link(version, file_name, data_folder)
        print(download_url)

    return download_url

def _get_azure_download_link(version_name: str, file_name: str) -> str:
    """
    Generates a publicly accessible download link for a file in Azure Blob Storage using a SAS token.

    Parameters:
    ----------
    version_name : str
        The name of the version or folder where the file is located.
    file_name : str
        The name of the file to be downloaded.

    Returns:
    -------
    str
        The publicly accessible download URL with SAS token for the file in Azure Blob Storage.
    """

    print("Generating SAS download link from Azure Blob Storage")

    blob_service_client = _azure_blob_service_client()
    container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
    blob_name = f"{version_name}/{file_name}"
    blob_client = container_client.get_blob_client(blob_name)

    print(f"Blob client for {version_name}/{file_name} created.")

    # Set expiration for SAS token (e.g., 1 hour from now)
    sas_token_expiry = datetime.now(timezone.utc) + timedelta(hours=1)
    print(f"SAS token expiry set to: {sas_token_expiry}")

    # Generate the SAS token for the blob
    try:
        sas_token = generate_blob_sas(
            account_name=AZURE_ACCOUNT_NAME,
            container_name=AZURE_CONTAINER_NAME,
            blob_name=f"{version_name}/{file_name}",
            account_key=AZURE_ACCOUNT_KEY,
            permission=BlobSasPermissions(read=True),  # Allow read access
            expiry=sas_token_expiry
        )
        print(f"SAS token generated: {sas_token}")
    except Exception as e:
        print(f"Error generating SAS token: {e}")
        return None

    # Combine the blob URL with the generated SAS token
    sas_url = f"{blob_client.url}?{sas_token}"
    print(f"Generated SAS URL: {sas_url}")

    return sas_url

def _get_local_download_link(version_name: str, file_name: str, data_folder: str) -> str:
    """
    Generates a local file path to serve the file.

    Parameters:
    ----------
    version_name : str
        The name of the version or folder where the file is located.
    file_name : str
        The name of the file to be downloaded.
    data_folder : str
        The base folder where the local files are stored.

    Returns:
    -------
    str
        The local file path.

    """

    print("get file LOcally")
    file_path = Path( data_folder) / version_name / file_name
    if not file_path.exists():
        raise FileNotFoundError(f"The file {file_name} does not exist locally.")
    
    return str(file_path)

def x_copy_files_local(selected_master_template: str, project_version: str):
    """Copy CSV files locally."""
    try:
        base_dir = Path(__file__).parent.parent / "data" / selected_master_template
        target_dir = Path(__file__).parent.parent / "data" / project_version
        
        # Ensure target directory exists
        target_dir.mkdir(parents=True, exist_ok=True)

        for file in base_dir.glob("*.csv"):
            target_file = target_dir / file.name
            target_file.write_text(file.read_text())
            logger.info(f"Copied {file.name} to {target_dir}")

    except Exception as e:
        logger.error(f"Failed to copy files locally: {str(e)}")
        raise

def _copy_files_local(selected_master_template: str, project_version: str):
    """Copy CSV, JPG, and PNG files locally."""
    try:
        base_dir = Path(__file__).parent.parent / "data" / selected_master_template
        target_dir = Path(__file__).parent.parent / "data" / project_version
        
        # Ensure target directory exists
        target_dir.mkdir(parents=True, exist_ok=True)

        # Glob for CSV, JPG, and PNG files
        for file in base_dir.glob("*.*"):
            if file.suffix in ['.csv', '.jpg', '.png']:
                target_file = target_dir / file.name
                target_file.write_bytes(file.read_bytes())  # Use read_bytes for binary files (images)
                logger.info(f"Copied {file.name} to {target_dir}")

    except Exception as e:
        logger.error(f"Failed to copy files locally: {str(e)}")
        raise



def _copy_files_azure(selected_master_template: str, project_version: str):
    """Copy CSV, JPG and PNG files in Azure Blob Storage."""
    try:
        blob_service_client = _azure_blob_service_client()
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)

        blobs = container_client.list_blobs(name_starts_with=f"{selected_master_template}/")

        for blob in blobs:
            if blob.name.endswith(('.csv', '.jpg', '.png')):
                # Copy each CSV file to the target directory
                source_blob = blob.name
                target_blob = f"{project_version}/{blob.name.split('/')[-1]}"
                blob_client = container_client.get_blob_client(target_blob)

                # Download the source blob
                download_stream = container_client.get_blob_client(source_blob).download_blob().readall()

                # Upload to the target location
                blob_client.upload_blob(download_stream, overwrite=True)
                logger.info(f"Copied {blob.name} to {target_blob}")

    except AzureError as e:
        logger.error(f"Azure error while copying files: {str(e)}")
        raise
    except ResourceExistsError as e:
        logger.warning(f"File already exists: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during file copy in Azure: {str(e)}")
        raise

    
def _azure_blob_service_client():
    """Creates and returns an Azure Blob service client using account name and key."""
    account_url = f"https://{AZURE_ACCOUNT_NAME}.blob.core.windows.net"
    return BlobServiceClient(account_url=account_url, credential=AZURE_ACCOUNT_KEY)


def _create_azure_directory(version_name):
    """Creates a directory in Azure Blob Storage."""
    try:
        blob_service_client = _azure_blob_service_client()
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        blob_name = f"{version_name}/.folder"  # Empty blob acts as a folder
        blob_client = container_client.get_blob_client(blob_name)
        blob_client.upload_blob("", overwrite=True)
        logger.info(f"Azure directory '{version_name}' created successfully.")
        return True
    except AzureError as e:
        logger.error(f"Azure error: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}")
        return False


def _create_local_directory(version_name):
    """Creates a local directory for storing files."""
    try:
        data_dir = Path(__file__).parent.parent / "data" / version_name
        data_dir.mkdir(parents=True, exist_ok=True)
        logger.info(f"Local directory '{version_name}' created successfully.")
        return True
    except Exception as e:
        logger.error(f"Failed to create local directory: {str(e)}")
        return False


def _upload_to_azure(file_content, version_name, file_name):
    """Uploads a file to Azure Blob Storage."""
    try:
        blob_service_client = _azure_blob_service_client()
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        blob_name = f"{version_name}/{file_name}"
        blob_client = container_client.get_blob_client(blob_name)

        if isinstance(file_content, str):
            file_content = file_content.encode('utf-8')

        blob_client.upload_blob(file_content, overwrite=True)
        return True
    except AzureError as e:
        logger.error(f"Azure error while saving file: {str(e)}")
        return False
    except Exception as e:
        logger.error(f"Unexpected error while saving file: {str(e)}")
        return False


def _store_locally(file_content, version_name, file_name):
    """Stores a file locally in the defined version directory."""
    try:
        data_dir = Path(__file__).parent.parent / "data" / version_name
        file_path = data_dir / file_name

        if isinstance(file_content, bytes):
            file_path.write_bytes(file_content)
        else:
            file_path.write_text(file_content, encoding='utf-8')

        return True
    except Exception as e:
        logger.error(f"Failed to save file locally: {str(e)}")
        return False

import pandas as pd
import io

def _load_from_azure(folder_name: str, file_name: str) -> pd.DataFrame:
    """
    Reads a file from Azure Blob Storage and returns its contents as a Pandas DataFrame.

    Parameters:
    ----------
    folder_name : str
        The folder in the Azure Blob Storage container where the file is located.
    file_name : str
        The name of the file to be loaded from Azure Blob Storage.

    Returns:
    -------
    pd.DataFrame
        The contents of the file as a Pandas DataFrame.

    Raises:
    -------
    ValueError:
        If the file extension is not supported.
    """
    try:
        # Create Blob service client
        blob_service_client = _azure_blob_service_client()
        container_client = blob_service_client.get_container_client(AZURE_CONTAINER_NAME)
        blob_name = f"{folder_name}/{file_name}"
        blob_client = container_client.get_blob_client(blob_name)
        
        download_stream = blob_client.download_blob().readall()

        if file_name.endswith('.csv'):
            return pd.read_csv(io.BytesIO(download_stream))
        elif file_name.endswith('.xlsx'):
            return pd.read_excel(io.BytesIO(download_stream))
        else:
            raise ValueError("Unsupported file type. Only .csv and .xlsx are supported.")
    
    except Exception as e:
        raise RuntimeError(f"Error reading file from Azure Blob: {str(e)}")


def _load_locally(version_name: str, file_name: str) -> pd.DataFrame:
    """
    Loads a CSV or Excel file from the local filesystem and returns its contents as a Pandas DataFrame.

    Parameters:
    ----------
    version_name : str
        The name of the version or folder where the file is located.
    file_name : str
        The name of the file to be loaded (should be a CSV or Excel file).

    Returns:
    -------
    pd.DataFrame
        The contents of the file as a Pandas DataFrame.

    Raises:
    -------
    FileNotFoundError:
        If the specified file does not exist.
    ValueError:
        If the file extension is not supported (only .csv and .xlsx).
    RuntimeError:
        For other errors encountered during file reading.

    Example:
    --------
    df = _load_locally("v1", "example.csv")
    """
    try:
        # Construct the file path
        data_dir = Path(__file__).parent.parent / "data" / version_name
        file_path = data_dir / file_name

        # Check if the file exists
        if not file_path.exists():
            raise FileNotFoundError(f"The file {file_path} does not exist.")

        # Read the file based on the file extension
        if file_name.endswith('.csv'):
            return pd.read_csv(file_path)
        elif file_name.endswith('.xlsx'):
            return pd.read_excel(file_path)
        else:
            raise ValueError("Unsupported file type. Only .csv and .xlsx are supported.")

    except FileNotFoundError as fnf_error:
        logger.error(f"File not found: {str(fnf_error)}")
        raise
    except ValueError as ve:
        logger.error(f"ValueError: {str(ve)}")
        raise
    except Exception as e:
        logger.error(f"Failed to load local file: {str(e)}")
        raise RuntimeError(f"An error occurred while reading the file: {str(e)}")

