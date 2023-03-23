import sys

from kilvin import log

try:
    import tomllib
except ModuleNotFoundError:
    import tomli as tomllib


def check_config(config):
    def keys_exist(keys):
        """Check for nested keys in config."""

        _elem = config
        for key in keys:
            try:
                _elem = _elem[key]
            except KeyError:
                return False
        return True

    keys = ["title", "url", "description", ["author", "name"], ["author", "email"]]
    is_incomplete = False
    for key in keys:
        if not isinstance(key, list):
            key = [key]

        if not keys_exist(key):
            is_incomplete = True
            key_str = ".".join(key)
            log.error(f'"{key_str}" not found in config.toml.')

    if is_incomplete:
        sys.exit(1)


def load_config():
    try:
        with open("config.toml", "rb") as cf:
            pass
            try:
                config = tomllib.load(cf)
                check_config(config)
                return config
            except tomllib.TOMLDecodeError:
                log.error("Something is wrong with the config file.")
                sys.exit(1)
    except FileNotFoundError as e:
        log.error(f"{e.filename} : {e.strerror}. Please add it.")
        sys.exit(1)
