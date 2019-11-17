# PyConfigMaker

![PyPI](https://img.shields.io/pypi/v/pyconfigmaker?label=PyConfigMaker&link=https://pypi.org/project/PyConfigMaker/)

A tiny package which automatically builds config objects and an argument parser from yaml script

[PyPi](https://pypi.org/project/PyConfigMaker/)
[Github](https://github.com/cvoelcker/PyConfigMaker)


A short usage example:

```
from sys import argv
from config_parser import config_parser

parser = config_parser.ConfigGenerator('sample_data/example.yml')
parsed = parser(argv[1:])
print(parsed)
print(parsed.PATHS.model_save_path)
parser.dump_config('test/test.yml')
```
