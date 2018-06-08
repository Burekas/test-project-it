import pathlib
import yaml

BASE_DIR = pathlib.Path(__file__).parent.parent
config_path = BASE_DIR / 'config' / 'config.yaml'


def get_config(path: pathlib.PosixPath) -> dict:
    """ Load yaml config"""
    with open(path) as f:
        config = yaml.load(f)
    return config


config = get_config(config_path)
