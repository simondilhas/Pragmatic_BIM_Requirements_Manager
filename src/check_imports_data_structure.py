import os
import pandas as pd
from typing import Dict, List

required_workflows_columns = [
    "WorkflowID",
    "WorkflowName*",
    "WorkflowSubheader*",
    "WorkflowDescription*",
    "Status",
]

required_models_columns = [
    "ModelID",
    "ModelName*",
    "ModelDescription*",
    "FileName*",
    "SortModels",
]

required_elements_columns = [
    "ElementID",
    "ElementName*",
    "SortElement",
    "IfcEntityIfc4.0Name",
    "ElementDescription*",
]

required_attributes_columns = [
    "AttributeID",
    "AttributeName",
    "SortAttribute",
    "AttributeDescription*",
    "Pset",
    "AllowedValues*",
    "RegexCheck*",
    "DataTyp",
    "Unit",
    "IFC2x3",
    "IFC4",
    "IFC4.3",
    "Applicability",
    "ElementID",
    "ModelID",
    "WorkflowID"
]

def check_required_columns(df: pd.DataFrame, required_columns: List[str], df_name: str) -> None:
    missing_columns = []
    for column in required_columns:
        if '*' in column:
            base_column = column[:-1]
            if not any(col.startswith(base_column) for col in df.columns):
                missing_columns.append(column)
        elif column not in df.columns:
            missing_columns.append(column)
    
    if missing_columns:
        raise ValueError(f"Missing required columns in {df_name}: {', '.join(missing_columns)}")