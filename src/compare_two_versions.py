
import pandas as pd
import os

#TODO: #5 Finish code and incorprate it into admin tools/page

v1 = 'SampleV.01'
v2 = 'SampleV.02'
data_dir_v1 = os.path.join('..', 'data', v1)
data_dir_v2 = os.path.join('..', 'data', v2)

def get_data_path() -> Path:
    if os.getenv('STREAMLIT_CLOUD'):
        return Path('/mount/src/pragmatic_bim_requirements_manager') / 'data' / VERSION
    else:
        return Path(__file__).parent.parent / 'data' / VERSION



file_name_attributes_v1 = os.path.join(data_dir_v1, 'Attributes-Export_All.csv')
file_name_attributes_v2 = os.path.join(data_dir_v2, 'Attributes-Export_All.csv')

print(f"Path 1: {file_name_attributes_v1}")
print(f"Path 2: {file_name_attributes_v2}")

#file_name_elements = os.path.join(data_dir, 'Elements-Export_All.csv')
#file_name_models = os.path.join(data_dir, 'Models-Export_All.csv')


df1 = pd.read_csv(file_name_attributes_v1)
df2 = pd.read_csv(file_name_attributes_v2)

# Compare the dataframes
comparison = df1.compare(df2)

# Output the differences
print(comparison)