import os
import json
from shutil import copyfile

class Configuration:
    _config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')

    if not os.path.isfile(_config_path):
        _config_sample_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json.sample')
        copyfile(_config_sample_path, _config_path)

    def get_config_data(self):
        with open(self._config_path, 'r') as config_file:
            config_string = config_file.read()
            return json.loads(config_string)
