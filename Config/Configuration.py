import yaml

config = {}


def get_config_by_key(key):
    global config

    if key not in config:
        with open("../Config/config.yaml", 'r') as stream:
            config = yaml.safe_load(stream)['polyschedule-bot']
            if key not in config:
                return None
            else:
                return config[key]
    return config[key]
