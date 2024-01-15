import yaml

def load():
    with open('config.yaml', 'r') as file:
        return yaml.safe_load(file)