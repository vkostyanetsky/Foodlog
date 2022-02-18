import os
import sys
import argparse

import modules.yaml_wrapper as yaml_wrapper

def get_arguments():

    args_parser = argparse.ArgumentParser()

    args_parser.add_argument(
        '--settings',
        type = str,
        help = 'the path to the settings file',
        required = True
    )
        
    return args_parser.parse_args()

def get_options():

    def get_options_filepath():

        def get_default_options_dirpath():

            script_dirpath = os.path.abspath(os.path.dirname(__file__))
            
            result = os.path.split(script_dirpath)[0]
            result = os.path.split(result)[0]
            
            return result

        def get_parameter(name: str, default_value: str = ''):
                        
            result = default_value

            for i, value in enumerate(sys.argv):

                if value == name and len(sys.argv) > i:

                    result = sys.argv[i + 1]
                    break

            return result

        default_options_dirpath     = get_default_options_dirpath()
        default_options_filename    = 'options.yaml'
        default_options_filepath    = os.path.join(default_options_dirpath, default_options_filename)

        return get_parameter('--options', default_options_filepath)

    options_filepath = get_options_filepath()

    result = yaml_wrapper.get_data_from_file(options_filepath)

    if result == None:
        result = []
                    
    return result    

def get_journal(options):

    result = yaml_wrapper.get_data_from_file(options['journal_filepath'])
        
    if result == None:
        result = []
                    
    return result

def get_catalog(options):

    result = yaml_wrapper.get_data_from_file(options['catalog_filepath'])
        
    if result == None:
        result = []
                    
    return result