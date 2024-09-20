import yaml

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