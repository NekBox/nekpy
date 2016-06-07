from os.path import exists, expanduser, join
import json
from .utils import Struct

class Configuration(Struct):
    def update(self, obj):
        if isinstance(obj, dict):
            self._attrs.update(obj)
        elif isinstance(obj, Struct):
            self._attrs.update(obj._attrs)

default_config = Configuration()
default_config.makenek = join(expanduser("~"), "NekBox/makenek")
default_config.legacy  = join(expanduser("~"), "Nek5000/core/makenek")
default_config.load    = join(expanduser("~"), "nek-analyze/load.py")
default_config.nekmpi  = join(expanduser("~"), "NekBox/bin/nekmpi")
default_config.tools   = join(expanduser("~"), "Nek5000/tools")

# grab defaults from config files
if exists(join(expanduser("~"), ".nekpy.json")):
  with open(join(expanduser("~"), ".nekpy.json")) as f:
    system_config = json.load(f)
else:
  with open(join(expanduser("~"), ".nekpy.json"), 'w') as f:
    json.dump(default_config._attrs, f, indent=4)
  print("Default configuration written to ~/.nekpy.json")
  system_config = {}

config = Configuration()
config.update(default_config)
config.update(system_config)

