import os

def find_file(name):
    current_dir = os.getcwd()
    root_dir = os.path.abspath(os.sep)

    while current_dir != root_dir:
        config_path = os.path.join(current_dir, name)
        if os.path.isfile(config_path):
            return config_path
        current_dir = os.path.dirname(current_dir)

    raise FileNotFoundError(f"{name} file not found in the project root directory.")