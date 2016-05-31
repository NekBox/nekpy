import json
from subprocess import check_output
from os.path import realpath, join, dirname
import shutil
from os import system

from pkg_resources import resource_string
from ..utils import Struct

mypath = (realpath(__file__))[:-9]

#with open(join(mypath, "default.json"), "r") as f:
#    default_config = json.load(f)
default_config = json.loads(resource_string("nekpy.tools", "default.json").decode())

with open(join(mypath, "template.SIZE"), "r") as f:
    size_template = f.read()

with open(join(mypath, "template.size_mod"), "r") as f:
    size_mod_template = f.read()

with open(join(mypath, "template.rea"), "r") as f:
    rea_template = f.read()

with open(join(mypath, "template.box"), "r") as f:
    box_template = f.read()

def genrun(name, config_in, tusr, 
        do_map=False, 
        do_clean=False, 
        do_make=False, 
        legacy=False, 
        makenek="makenek",
        tools=None):

    config = {}
    config.update(default_config)
    config.update(config_in)

    legacy = legacy or "legacy" in config_in

    with open("{:s}.json".format(name), "w") as f:
        json.dump(config, f, indent=2)

    ''' Computing stuff '''

    # loads the configuration into current variable scope
    c = Struct(config)

    c.dealiasing_order = c.order * 3 / 2
    c.ltorder = abs(c.torder)

    # Manipulate the configuration here
    c.elements_total = c.shape_mesh[0] * c.shape_mesh[1] * c.shape_mesh[2]

    if c.left_bound == 'P':
        c.left_boundv = 'P'

    if c.right_bound == 'P':
        c.right_boundv = 'P'

    if c.front_bound == 'P':
        c.front_boundv = 'P'

    if c.back_bound == 'P':
        c.back_boundv = 'P'

    if c.top_bound == 'P':
        c.top_boundv = 'P'

    if c.bottom_bound == 'P':
        c.bottom_boundv = 'P'

    # writes the current variable scope to the configuration
    config = c._attrs

    ''' Writing stuff '''

    size = size_template.format(**config)
    with open("SIZE", "w") as f:
        f.write(size)

    size = size_mod_template.format(**config)
    with open("size_mod.F90", "w") as f:
        f.write(size)

    rea = rea_template.format(**config)
    with open("{:s}.rea".format(name), "w") as f:
        f.write(rea)

    box = box_template.format(**config)
    with open("{:s}.box".format(name), "w") as f:
        f.write(box)
    
    usr = tusr.format(**config)
    with open("{:s}.usr".format(name), "w") as f:
        f.write(usr)

    if legacy:
        shutil.copy("./{:s}.rea".format(name), "./tmp.rea".format(name))
        system("echo './{:s}.box' | {}".format(name, "genbox"))
        shutil.copy("./box.rea", "./{:s}.rea".format(name))
        with open(".tmp", "w") as f:
            f.write("{:s}\n0.01\n".format(name))
        system("genmap < .tmp")

    log = ""
    if do_clean:
        cmd = [makenek, "clean" , dirname(makenek)]
        log += check_output(cmd).decode() + "\n"

    if do_make:
        print(makenek, name, dirname(makenek))
        cmd = [makenek, name, dirname(makenek)]
        log += check_output(cmd).decode()

    return log
