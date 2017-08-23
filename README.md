## What is this repo?
Task here is to plot determine mean movie length by country and plot it on a map.

### Steps
1. Obtain IMDB data in list format (Files obtained: countries, language, movies and running-times)
2. Use modified [imdb2json.py](https://github.com/oxplot/imdb2json/blob/master/imdb2json.py) with [convert_IMDB_list_to_json.py](../src/convert_IMDB_list_to_json.py)
to convert IMDB list format to JSON format. Note: Modified imdb2json.py is not made available here as I am not certain about its license terms
3. Convert JSON data to TSV format using [convert_IMDB_json_to_tsv.py](../src/convert_IMDB_json_to_tsv.py)
4. Combine TSV data obtained from multiple IMDB files using [analyze_imdb_data.ipynb](../analysis/analyze_imdb_data.ipynb) and determine mean movie runtime by country
5. Plot it on map using [plot_imdb_runtime_on_map.ipynb](../analysis/plot_imdb_runtime_on_map.ipynb)

### License
Code in this repository is distributed under MIT license.