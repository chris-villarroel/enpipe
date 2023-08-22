import os
import subprocess
import yaml

def read_yaml_file(yaml_path):
    """
    Function to read a YAML file and return it as a dictionary.

    Parameters:
    yaml_path (str): The path to the YAML file.

    Returns:
    dict: The YAML file as a Python dictionary.
    """
    with open(yaml_path) as f:
        config = yaml.safe_load(f)
    return config

def write_yaml_file(yaml_path, data):
    """
    Function to write a dictionary to a YAML file.

    Parameters:
    yaml_path (str): The path to the YAML file.
    data (dict): The data to be written to the file.
    """
    with open(yaml_path, 'w') as f:
        yaml.safe_dump(data, f)

def read_env_file(env_path=".env"):
    """
    Function to read an environment file and return it as a dictionary.

    Parameters:
    env_path (str): The path to the environment file. Defaults to ".env".

    Returns:
    dict: The environment file as a Python dictionary.
    """
    if os.path.exists(env_path):
        with open(env_path) as f:
            env_vars = dict(line.strip().split('=', 1) for line in f if line.strip())
    elif os.path.exists("tests/fixtures/" + env_path):
        with open("tests/fixtures/" + env_path) as f:
            env_vars = dict(line.strip().split('=', 1) for line in f if line.strip())
    else:
        env_vars = {}

    if 'version' not in env_vars:
        yaml_file = 'config.yaml'
        if os.path.exists(yaml_file):
            with open(yaml_file) as f:
                yaml_data = yaml.safe_load(f)
                if 'version' in yaml_data:
                    env_vars['version'] = yaml_data['version']

    return env_vars

def replace_placeholder_in_config(data, placeholder, replace_value):
    """
    Function to replace a placeholder in a configuration dictionary.

    Parameters:
    data (dict): The configuration dictionary.
    placeholder (str): The placeholder to be replaced.
    replace_value (str): The value to replace the placeholder.

    Returns:
    dict: The configuration dictionary with the placeholder replaced.
    """
    if isinstance(data, dict):
        for k, v in data.items():
            data[k] = replace_placeholder_in_config(v, placeholder, replace_value)
        return data
    elif isinstance(data, str):
        return data.replace(placeholder, replace_value)
    else:
        return data

def read_env_variable(file_path, variable_name, default_value=None):
    """
    Function to read an environment variable from a file.

    Parameters:
    file_path (str): The path to the file.
    variable_name (str): The name of the variable.
    default_value (str, optional): The default value of the variable if not found. Defaults to None.

    Returns:
    str: The value of the environment variable.
    """
    if os.path.exists(file_path):
        with open(file_path) as f:
            for line in f:
                if line.startswith(variable_name + '='):
                    return line[len(variable_name) + 1:].strip()
    if default_value is not None:
        return default_value
    raise ValueError(f"Variable {variable_name} not found in {file_path} and no default value provided")

def run_cmd(cmd):
    """
    Function to run a command using subprocess.

    Parameters:
    cmd (str): The command to be run.
    """
    subprocess.run(cmd, shell=True, check=True)

def prepare_cmd_args(params=None, input=None, output=None):
    """
    Function to prepare command line arguments.

    Parameters:
    params (dict, optional): The parameters for the command. Defaults to None.
    input (dict, optional): The input for the command. Defaults to None.
    output (dict, optional): The output for the command. Defaults to None.

    Returns:
    str: The command line arguments as a string.
    """
    cmd_line_str = ""

    if params:
        for key, value in params.items():
            cmd_line_str += f"--{key} {value} "

    if input:
        for key, value in input.items():
            if key == "script":
                continue
            cmd_line_str += f"--{key} {value} "

    if output:
        for key, value in output.items():
            cmd_line_str += f"--{key} {value} "

    return cmd_line_str.strip()

def read_config(yaml_path):
    """
    Function to read a configuration from a YAML file and replace placeholders.

    Parameters:
    yaml_path (str): The path to the YAML file.

    Returns:
    dict: The configuration from the YAML file with placeholders replaced.
    """
    config = read_yaml_file(yaml_path)
    env_vars = read_env_file()
    if "version" in env_vars:
        config = replace_placeholder_in_config(config, "{version}", env_vars["version"])
    
    return config

