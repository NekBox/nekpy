from os.path import exists, expanduser, join
import json

class Struct:
    """Masquerade a dictionary with a structure-like behavior."""
    """From gprof2dot.py"""

    def __init__(self, attrs = None):
        if attrs is None:
            attrs = {}
        self.__dict__['_attrs'] = attrs

    def __getattr__(self, name):
        try:
            return self._attrs[name]
        except KeyError:
            raise AttributeError(name)

    def __setattr__(self, name, value):
        self._attrs[name] = value

    def __str__(self):
        return str(self._attrs)

    def __repr__(self):
        return repr(self._attrs)


class Configuration(Struct):
    def update(self, obj):
        if isinstance(obj, dict):
            self._attrs.update(obj)
        elif isinstance(obj, Struct):
            self._attrs.update(obj._attrs)

default_config = Configuration()
default_config.makenek = join(expanduser("~"), "NekBox/makenek")
default_config.load    = join(expanduser("~"), "nek-analyze/load.py")
default_config.nekmpi  = join(expanduser("~"), "NekBox/nekmpi")
default_config.genrun  = join(expanduser("~"), "nek-tools/genrun/genrun.py")

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

