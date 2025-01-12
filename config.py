import json
import os

CONFIG_FILE = os.path.join(os.path.dirname(__file__), 'config.json')
DEFAULT_CONFIG = {
    "circle_params": {
        "dp": 1.2,
        "minDist": 1000,
        "param1": 100,
        "param2": 30,
        "minRadius": 150,
        "maxRadius": 300
    },
    "output_params": {
        "video_format": "mp4",  
        "image_format": "jpg" 
    }
}

def load_config():
    """
    Loads configuration from config.json.
    If the file doesn't exist or is corrupt, create or overwrite with defaults.
    Returns a tuple: (circle_params, output_params)
    """
    if not os.path.isfile(CONFIG_FILE):
        save_config(DEFAULT_CONFIG["circle_params"], DEFAULT_CONFIG["output_params"])
        return DEFAULT_CONFIG["circle_params"], DEFAULT_CONFIG["output_params"]

    try:
        with open(CONFIG_FILE, 'r') as f:
            config_data = json.load(f)
        circle_params = config_data.get("circle_params", DEFAULT_CONFIG["circle_params"])
        output_params = config_data.get("output_params", DEFAULT_CONFIG["output_params"])

        for key in DEFAULT_CONFIG["circle_params"].keys():
            if key not in circle_params:
                circle_params[key] = DEFAULT_CONFIG["circle_params"][key]
        for key in DEFAULT_CONFIG["output_params"].keys():
            if key not in output_params:
                output_params[key] = DEFAULT_CONFIG["output_params"][key]

        return circle_params, output_params
    except (ValueError, json.JSONDecodeError):
        save_config(DEFAULT_CONFIG["circle_params"], DEFAULT_CONFIG["output_params"])
        return DEFAULT_CONFIG["circle_params"], DEFAULT_CONFIG["output_params"]

def save_config(circle_params, output_params):
    """
    Saves the provided circle_params and output_params to config.json.
    """
    config_data = {
        "circle_params": circle_params,
        "output_params": output_params
    }
    with open(CONFIG_FILE, 'w') as f:
        json.dump(config_data, f, indent=4)
