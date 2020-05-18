import pickle
import yaml


def load_yaml(path):
    """
    YAML requires a loader. The documentation suggests using CLoader, if it's available, over Loader for performance.
    https://pyyaml.org/wiki/PyYAMLDocumentation
    """
    try:
        loader = yaml.CLoader
    except:
        loader = yaml.Loader

    if not path.endswith(".yaml"):
        path += ".yaml"
    with open(path, encoding="utf8") as file:
        data = yaml.load(file, Loader=loader)
    return data


def save_yaml(data, path):
    """
    YAML requires a loader. The documentation suggests using CLoader, if it's available, over Loader for performance.
    https://pyyaml.org/wiki/PyYAMLDocumentation
    """
    try:
        dumper = yaml.CDumper
    except:
        dumper = yaml.Dumper

    if not path.endswith(".yaml"):
        path += ".yaml"
    with open(path, "w", encoding="utf8") as file:
        yaml.dump(data, file, Dumper=dumper)


def load_pickle(path):
    if not path.endswith(".pickle"):
        path += ".pickle"
    with open(path, "rb") as file:
        data = pickle.load(file)
    return data


def save_pickle(data, path):
    if not path.endswith(".pickle"):
        path += ".pickle"
    with open(path, "wb") as file:
        pickle.dump(data, file)
