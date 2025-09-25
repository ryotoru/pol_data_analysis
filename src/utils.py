import yaml 
import os 

def load_config(config_path: str) -> dict:
    """Load config from YAML file."""
    if not os.path.exists(config_path):
        print(f"Config file '{config_path}' does not exist.\n Proceeding with defult/CLI args")
        return {}
    with open(config_path, 'r') as f:
        config = yaml.safe_load(f)
    return config if config is not None else {}