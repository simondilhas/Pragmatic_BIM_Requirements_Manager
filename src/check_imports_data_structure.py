import os
import sys
import pandas as pd
from typing import Dict, List
import yaml

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

with open("config.yaml", "r") as file:
    config_data = yaml.safe_load(file)

required_workflows_columns = config_data["required_workflows_columns"]
required_models_columns = config_data["required_models_columns"]
required_elements_columns = config_data["required_elements_columns"]
required_attributes_columns = config_data["required_attributes_columns"]

def check_required_columns(df: pd.DataFrame, required_columns: List[str]) -> None:
    missing_columns = []
    for column in required_columns:
        if '*' in column:
            base_column = column[:-1]
            if not any(col.startswith(base_column) for col in df.columns):
                missing_columns.append(column)
        elif column not in df.columns:
            missing_columns.append(column)
    
    if missing_columns:
        #raise ValueError(f"Missing required columns: {', '.join(missing_columns)}")
        return (f"Missing required columns: {', '.join(missing_columns)}")
    
