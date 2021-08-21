import os
import modules.yaml_wrapper as yaml_wrapper

def get_settings(dirpath):

    filepath = os.path.join(dirpath, 'tuner.yaml')

    return yaml_wrapper.get_data_from_file(filepath)