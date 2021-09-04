import os
import modules.yaml_wrapper as yaml_wrapper

def get_options(dirpath):

    filepath = os.path.join(dirpath, 'options.yaml')

    return yaml_wrapper.get_data_from_file(filepath)

def get_journal(dirpath, settings):

    journal_filepath = os.path.join(dirpath, settings['journal_filename'])

    result = yaml_wrapper.get_data_from_file(journal_filepath)
        
    if result == None:
        result = []
                    
    return result

def get_catalog(dirpath, settings):

    catalog_filepath = os.path.join(dirpath, settings['catalog_filename'])

    result = yaml_wrapper.get_data_from_file(catalog_filepath)
        
    if result == None:
        result = []
                    
    return result