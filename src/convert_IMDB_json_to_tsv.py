'''
Reads IMDB data in JSON format and converts it to TSV format

Author: Mana G
'''

import json
import csv
import os
import glob
import gzip

def set_column_names(basename):
    if basename.startswith('running-times'):
        fieldnames = ['id', 'kind', 'title', 'episode', 'running_times', 'running_times_first', 'running_times_rest']
    elif basename.startswith('language'):
        fieldnames = ['id', 'kind', 'title', 'episode', 'suspended', 'languages', 'languages_first', 'languages_rest']
    elif basename.startswith('movies'):
        fieldnames = ['id', 'kind', 'title', 'episode', 'year', 'year_first', 'year_rest']
    elif basename.startswith('countries'):
        fieldnames = ['id', 'kind', 'title', 'episode', 'countries', 'countries_first', 'countries_rest']
    else:
        print('Unknown IMDB file name. Resolve this.')
        exit()
    return fieldnames

# divide column of interest into first language and the rest, if in dict form
def process_field_as_dict(json_dict, colname, key):
    languages = json_dict[colname]
    # print (languages)
    if key in languages[0]:
        json_dict['%s_first' %colname] = languages[0][key]
    else:
        json_dict['%s_first' % colname] = 'NA'
        print('Key %s not available in column %s' % (key, colname))
        print ('\t%s' % languages)

    rest_languages = set()
    if len(languages) > 1:
        for item in languages[1:]:
            if key in item:
                rest_languages.add(item[key])

    json_dict['%s_rest' %colname] = ','.join([str(x) for x in rest_languages])

    return json_dict


# divide column of interest into first language and the rest, if in list form
def process_field_as_list(json_dict, colname):
    field_data = json_dict[colname]
    field_data = [x  for x in field_data  if not x is None]

    first_col = '%s_first' % colname
    rest_col = '%s_rest' % colname
    json_dict[first_col] = ''
    json_dict[rest_col] = ''

    if len(field_data) > 0:
        json_dict[first_col] = field_data[0]
        json_dict[rest_col] = ','.join([str(x) for x in field_data[1:]])

    return json_dict

if __name__ == '__main__':
    # file_type = 'sample_data'
    file_type = 'complete'

    # get filenames and set output directory
    if file_type == 'sample_data':  # sample data
        imdb_json_dir = '../results/intermediate/samples/list2json'
        out_dir = '../results/intermediate/samples/json2tsv'
        imdb_json_files = glob.glob('%s/*.json.gz' % imdb_json_dir)
    elif file_type == 'complete':  # complete data
        imdb_json_dir = '../results/intermediate/complete/list2json'
        out_dir = '../results/intermediate/complete/json2tsv'
        imdb_json_files = glob.glob('%s/*.json.gz' % imdb_json_dir)
    else:
        print('Allowed options for variable "file_type": sample_data or complete')
        exit()


    # read imdb data in json form to tsv format
    for index, imdb_json_f in enumerate(imdb_json_files):
        print('Processing %i/%i:  %s' % (index + 1, len(imdb_json_files), imdb_json_f))
        basename = os.path.basename(imdb_json_f)
        json_out_tsv_f = os.path.join(out_dir, '%s.json.gz' % os.path.splitext(basename)[0])


        basename = os.path.basename(imdb_json_f)
        if 'sample' in basename:
            out_dir = '../results/intermediate/samples/json2tsv'
        else:
            out_dir = '../results/intermediate/complete/json2tsv'
        out_tsv_f = os.path.join(out_dir, basename.replace('json.gz', 'tsv.gz'))

        imdb_files = []
        error_count = 0
        with gzip.open(imdb_json_f, 'rb') as fd, gzip.open(out_tsv_f, 'wt', newline='') as tsv_out:
            fieldnames = set_column_names(basename)     # get column titles
            csv_writer = csv.DictWriter(tsv_out, fieldnames=fieldnames, delimiter='\t', extrasaction ='ignore')
            csv_writer.writeheader()
    
            for line in fd:
                json_data = json.loads(line)
                # print(json_data.keys())
                # print ('\t%s' % json_data['countries'])

                if json_data['kind'] == 'movie':      # includes only 'movies' as inclusion of other kinds unnecessarily increases memory requirement during data-processing
                    if basename.startswith('running-times'):
                        json_data = process_field_as_dict(json_data, colname='running_times', key='secs')
                    elif  basename.startswith('language'):
                        json_data = process_field_as_dict(json_data, colname='languages', key='name')
                    elif basename.startswith('countries'):
                        json_data = process_field_as_list(json_data, colname='countries')
                    elif basename.startswith('movies'):
                        json_data = process_field_as_list(json_data, colname='year')


                    try:
                        csv_writer.writerow(json_data)
                    except UnicodeEncodeError:
                        error_count += 1

        print ('\tTotal resulted in error during CSV writing: %i' % error_count)
    
