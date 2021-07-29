import yaml

def get_data_from_file(yaml_filepath):

    with open(yaml_filepath, encoding = 'utf-8-sig') as yaml_file:
        result = yaml.safe_load(yaml_file)    

    return result

def put_data_to_file(yaml_filepath, yaml_data):

    with open(yaml_filepath, 'w') as yaml_file:        
        yaml.dump(yaml_data, yaml_file, default_flow_style = False)