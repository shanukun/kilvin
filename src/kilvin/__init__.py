__version__ = "0.1"

import pathlib

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib



def check_config(config):
    def keys_exist(*keys):
        _elem = config
        for key in keys:
            try:
                _elem = _elem[key]
            except KeyError:
                return False
        return True

    keys = ["title", "url", "description", ["author", "name"], ["author", "email"]]
    for key in keys:
        if not keys_exist(*key):
            print(f"{key} not found. Please add {key} to config.")

def load_config():
    if not pathlib.Path("config.toml").exists():
        print("Config file not found.")
    else:

        with open("config.toml", "rb") as cf:
            try:
                config = tomllib.load(cf)
                check_config(config)
                return config
            except tomllib.TOMLDecodeError:
                print("Something is wrong with the config file.")


config = load_config()
