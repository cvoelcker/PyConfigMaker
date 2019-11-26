from collections import namedtuple
from typing import Dict, List, Type, Tuple, Optional
import argparse
import yaml


def parse_from_file(file_location: str) -> Dict:
    """
    Parses a yml file into a dict
    :param file_location: relative file location of the yml
    :return: the config dictionary
    """
    with open(file_location) as yaml_file:
        return yaml.safe_load(yaml_file)


def write_to_file(data: Dict, file_location: str):
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
    def __init__(self, yaml_file_location: str):
        """
        Initializes the config generator from a yml file location
        :param yaml_file_location: relative file location of the yaml config
        """
        self.config_dict = parse_from_file(yaml_file_location)
        self.tuple_templates = self.build_tuples()
        self.arg_parser = self.build_arg_parser()
        self.args: Optional[Dict] = None
    
    def __call__(self, args: List):
        """
        Parses the arguments. Needs to be called with sys.argv[1:] in general
        :param args: the argument (normally sys.argv[1:])
        :return: a dictionary of namedtuples filled with the defaults and the passed arguments
        """
        self.args = vars(self.arg_parser.parse_args(args))
        return self.build_config()

    def build_tuples(self):
        """
        Builds a dictionary of namedtuples for easier config access
        :return: a dictionary of namedtuples from the config dictionary, and a tuple to hold all
            config tuples
        """
        return self.build_tuples_rec('Config', self.config_dict)

    def build_tuples_rec(self, key, config_dict):
        all_tuples = {}
        for k in config_dict:
            if isinstance(config_dict[k], dict):
                all_tuples[k] = self.build_tuples_rec(k, config_dict[k])
        return namedtuple(key, config_dict.keys()), all_tuples
    
    def build_arg_parser(self) -> argparse.ArgumentParser:
        """
        Builds the argument parser with default values from the config file
        :return: the argument parser
        """
        parser = argparse.ArgumentParser(
                description='Process args for experiments', 
                formatter_class=argparse.ArgumentDefaultsHelpFormatter)
        self.build_arg_parser_rec(self.config_dict, parser)
        return parser

    def build_arg_parser_rec(self, config_dict, group):
        for k, v in config_dict.items():
            # recurse on dict
            if isinstance(v, dict):
                sub_group = group.add_argument_group(k)
                self.build_arg_parser_rec(v, sub_group)

            # setup code for boolean handling
            elif type(v) == bool:
                bool_group = group.add_mutually_exclusive_group(required=False)
                bool_group.add_argument('--' + k.replace('_', '-'), dest=k, default=v, action='store_true', help=' ')
                bool_group.add_argument('--no-' + k.replace('_', '-'), dest=k, default=v, action='store_false', help=' ')

            # setup fix code for list handling
            elif type(v) == list:
                try:
                    list_item_type = type(v[0])
                except IndexError as e:
                    print('Cannot parse default type from list without items')
                group.add_argument('--' + k.replace('_', '-'), nargs='+', default=v, type=list_item_type, help=' ')

            else:
                group.add_argument('--' + k.replace('_', '-'), default=v, type=type(v), help=' ')

    def build_config(self):
        """
        Builds the config, iterating over the internal dict and replacing values from the dict with
        the parsed arguments as needed
        :return: a dictionary of namedtuples containing the generated config
        """
        if self.args is None:
            raise ValueError('ConfigGenerator has no parsed arguments')
        arg_dict = self.args
        tuple_config, dict_config = self.build_config_rec(arg_dict, self.config_dict, self.tuple_templates)
        self.config_dict = dict_config
        return tuple_config

    def build_config_rec(self, arg_dict, config_dict, templates):
        used_config = dict()
        dict_config = dict()
        for k, v in config_dict.items():
            if isinstance(v, dict):
                used_config[k], dict_config[k] = self.build_config_rec(arg_dict, v, templates[1][k])
            elif k in arg_dict:
                used_config[k] = dict_config[k] = arg_dict[k]
            else:
                used_config[k] = dict_config[k] = v
        return templates[0](**used_config), dict_config

    def append_argument_to_config(self, argument_path, default):
        d = self.config_dict
        for a in argument_path[:-1]:
            d = d[a]
        d[argument_path[-1]] = default

    def recompile(self):
        self.tuple_templates = self.build_tuples()
        self.arg_parser = self.build_arg_parser()
        self.args: Optional[Dict] = None
    
    def dump_config(self, file_location: str):
        """
        Writes the config back to a file in yml format, which can be loaded again
        :param file_location: the relative file location
        """
        if self.args is None:
            raise ValueError('ConfigGenerator has no parsed arguments')
        arg_dict = self.args
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
