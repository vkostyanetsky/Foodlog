import os
import modules.yaml_wrapper as yaml_wrapper

def get_settings(script_dirpath):

    filepath = os.path.join(script_dirpath, 'settings.yaml')

    return yaml_wrapper.get_data_from_file(filepath)