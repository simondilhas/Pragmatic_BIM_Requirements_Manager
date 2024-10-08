import yaml
import json
from pathlib import Path
from typing import List, Dict
import streamlit as st
import zipfile


def load_config(file_path='config.yaml'):
    """
    Loads the configuration from a YAML file.
    
    Parameters:
    file_path (str): The path to the YAML configuration file.
    
    Returns:
    dict: A dictionary containing the configuration.
    """
    try:
        with open(file_path, 'r') as yaml_file:
            config = yaml.safe_load(yaml_file)
        return config
    except FileNotFoundError:
        print(f"Error: {file_path} not found.")
        return {}
    except yaml.YAMLError as e:
        print(f"Error parsing YAML file: {e}")
        return {}
    
@st.cache_data
def load_translations(json_path: Path) -> Dict:
    with open(json_path, 'r', encoding='utf-8') as file:
        return json.load(file)
    
def extract_zip(zip_file, extract_to):
    with zipfile.ZipFile(zip_file, 'r') as zip_ref:
        zip_ref.extractall(extract_to)