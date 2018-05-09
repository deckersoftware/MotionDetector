import os
import json

class configuration:
    config_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), 'config.json')

    def get_config_data(self):
        with open(self.config_path, 'r') as config_file:
            config_string = config_file.read()
            return json.loads(config_string)