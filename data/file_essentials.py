import json

# general json loader
def get_json(path):
    file = open(path)
    json_as_dict = json.load(file)
    file.close()
    return json_as_dict

# load a file from the configs folder
def get_configs(config_filename): return get_json('data/configs/' + config_filename + '.json')