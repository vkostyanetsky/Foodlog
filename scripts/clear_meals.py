import os
import shutil
import datetime

import modules.common_logic as common_logic
import modules.yaml_wrapper as yaml_wrapper

def get_archive_filename():

    date = datetime.datetime.today() - datetime.timedelta(days = 1)
    date = date.strftime('%Y-%m-%d')

    return '{}.yaml'.format(date)

script_dirpath  = os.path.abspath(os.path.dirname(__file__))
dirpath         = os.path.split(script_dirpath)[0]

settings = common_logic.get_settings(dirpath)

journal_filepath    = os.path.join(dirpath, settings['journal_filename'])
journal             = yaml_wrapper.get_data_from_file(journal_filepath)

if journal != None:

    archive_filename = get_archive_filename()
    archive_filepath = os.path.join(dirpath, settings['archive_dirname'], archive_filename)

    if os.path.exists(archive_filepath):

        print("Журнал уже сохранен в архиве!")

    else:

        shutil.copyfile(journal_filepath, archive_filepath)
        open(journal_filepath, 'w').close()