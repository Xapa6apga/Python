import yaml


class ReadConfig:
    def __init__(self, path):
        with open(path, 'r') as cfg_file:
            self.config = yaml.safe_load(cfg_file)

    def get_config(self, app):
        return self.config[app]
