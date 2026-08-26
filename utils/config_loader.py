import yaml
from pathlib import Path
import os


def load_config():
    """
    Load the configuration from the config.yaml file.
    """
    config_path = "config/config.yaml"
    with open(config_path, "r") as f:
        config = yaml.safe_load(f)
    return config

