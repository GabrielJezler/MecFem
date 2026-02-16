import toml

def load_colors():
    return toml.load(r"src/assets/colors.toml")

def load_config():
    return toml.load(r"src/assets/config.toml")

def update_config(new_config: dict):
    with open(r"src/assets/config.toml", "w") as f:
        toml.dump(new_config, f)