import yaml

def get_data_from_file(yaml_filepath):

    with open(yaml_filepath, encoding = 'utf-8-sig') as yaml_file:
        result = yaml.safe_load(yaml_file)    

    return result