from collections import namedtuple
import argparse
import yaml


def parse_from_file(file_location):
    """
    Parses a yml file into a dict
    :param file_location: relative file location of the yml
    :return: the config dictionary
    """
    with open(file_location) as yaml_file:
        return yaml.safe_load(yaml_file)


def write_to_file(data, file_location):
    """
    Writes a dictionary back into yml format
    :param data: the dictionary
    :param file_location: relative file location
    """
    with open(file_location, 'w') as outfile:
        yaml.dump(data, outfile, default_flow_style=False)


class ConfigGenerator:
    """
    Holds the parser, yml config dict and the tuple templates
    """
    def __init__(self, yaml_file_location):
        """
        Initializes the config generator from a yml file location
        :param yaml_file_location: relative file location of the yaml config
        """
        self.config_dict = parse_from_file(yaml_file_location)
        self.storage_tuples = self.build_tuples()
        self.arg_parser = self.build_arg_parser()
        self.args = None
    
    def __call__(self, args):
        """
        Parses the arguments. Needs to be called with sys.argv[1:] in general
        :param args: the argument (normally sys.argv[1:])
        :return: a dictionary of namedtuples filled with the defaults and the passed arguments
        """
        self.args = self.arg_parser.parse_args(args)
        return self.build_config()

    def build_tuples(self):
        """
        Builds a dictionary of namedtuples for easier config access
        :return: a dictionary of namedtuples from the config dictionary
        """
        all_tuples = {}
        for k in self.config_dict:
            config_tuple = namedtuple(k, self.config_dict[k].keys())
            all_tuples[k] = config_tuple
        return all_tuples
    
    def build_arg_parser(self):
        """
        Builds the argument parser with default values from the config file
        :return: the argument parser
        """
        parser = argparse.ArgumentParser(
                description='Process args for experiments', 
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        for config in self.config_dict:
            group = parser.add_argument_group(config)
            for k, v in self.config_dict[config].items():
                group.add_argument('--' + k, default=v, type=type(v))
        return parser

    def build_config(self):
        """
        Builds the config, iterating over the internal dict and replacing values from the dict with
        the parsed arguments as needed
        :return: a dictionary of namedtuples containing the generated config
        """
        if self.args is None:
            raise ValueError('ConfigGenerator has no parsed arguments')
        arg_dict = vars(self.args)
        all_config_templates = dict()
        for c in self.config_dict:
            config = {}
            for k, v in self.config_dict[c].items():
                if k in arg_dict:
                    config[k] = arg_dict[k]
                else:
                    config[k] = v
            all_config_templates[c] = self.storage_tuples[c](**config)
        return all_config_templates
    
    def dump_config(self, file_location):
        """
        Writes the config back to a file in yml format, which can be loaded again
        :param file_location: the relative file location
        """
        arg_dict = vars(self.args)
        save_dict = dict()
        for c in self.config_dict:
            save_dict_section = {}
            for k, v in self.config_dict[c].items():
                if k in arg_dict:
                    save_dict_section[k] = arg_dict[k]
                else:
                    save_dict_section[k] = v
            save_dict[c] = save_dict_section
        write_to_file(save_dict, file_location)
