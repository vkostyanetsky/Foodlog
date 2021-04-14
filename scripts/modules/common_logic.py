import os
import modules.yaml_wrapper as yaml_wrapper

def get_options(dirpath):

    filepath = os.path.join(dirpath, 'options.yaml')

    return yaml_wrapper.get_data_from_file(filepath)