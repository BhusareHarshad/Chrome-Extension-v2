import yaml

def read_yaml(file_path):
    with open(file_path, 'r') as yaml_file:
        try:
            data = yaml.safe_load(yaml_file)
            return data
        except yaml.YAMLError as e:
            print(f"Error reading YAML file: {e}")