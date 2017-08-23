'''
Convert IMDB list files to JSON using in-house edited imdb2json.py (from https://github.com/oxplot/imdb2json)

Author: Mana G
'''

import subprocess
import glob
import os

if __name__ == '__main__':
    file_type = 'sample_data'
    # file_type = 'complete'

    # get filenames and set output directory
    if file_type == 'sample_data':      # sample data
        imdb_list_dir = '../data/imdb_samples'
        out_dir = '../results/intermediate/samples/list2json'
        imdb_files = glob.glob('%s/*.list' % imdb_list_dir)
    elif file_type == 'complete':       # complete data
        imdb_list_dir = '../data/imdb'
        out_dir = '../results/intermediate/complete/list2json'
        imdb_files = glob.glob('%s/*.list.gz' % imdb_list_dir)
    else:
        print('Allowed options for variable "file_type": sample_data or complete')
        exit()


    # call imdb2json_manaEdited.py to convert list files to json
    for index, imdb_list_f in enumerate(imdb_files):
        print ('Processing %i/%i:  %s' % (index+1, len(imdb_files), imdb_list_f))
        basename = os.path.basename(imdb_list_f)
        json_out_f = os.path.join(out_dir, '%s.json.gz' % os.path.splitext(basename)[0])

        subprocess.call(['python', 'imdb2json_manaEdited.py', '-o', json_out_f, 'convert', 'title', imdb_list_f])
