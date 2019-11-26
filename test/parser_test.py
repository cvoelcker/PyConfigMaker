from sys import argv
from config_parser import config_parser

parser = config_parser.ConfigGenerator('sample_data/example.yml')
parsed = parser(argv[1:])
print(parsed)
print(parsed.PATHS.model_save_path)
parser.dump_config('test/test_2.yml')

parser = config_parser.ConfigGenerator('test/test.yml')
parsed = parser(argv[1:])
print(parsed)
print(parsed.PATHS.model_save_path)
parser.dump_config('test/test_3.yml')
