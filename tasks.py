#!/home/maxhutch/anaconda3/bin/python3

import json
from os import chdir, makedirs
from dask.imperative import delayed, value
from subprocess import call, check_output, DEVNULL
from copy import deepcopy


def configure(base, override, workdir):
    res = deepcopy(base)
    res = dict(list(res.items()) + list(override.items()))
    res["workdir"] = workdir
    if res["io_step"] == 0:
        res["io_step"] = 100000000
    return res 

@delayed
def prepare(base, tusr):
    try:
        makedirs(base["workdir"])
    except OSError:
        pass
    chdir(base["workdir"]) 
    with open("cf.json", "w") as f:
        json.dump(base, f, indent=2)

    cmd = ["/home/maxhutch/src/nek-tools/genrun/genrun.py", "-d",  "./cf.json", "-u",  "{}".format(tusr), "--makenek=/home/maxhutch/src/NekBox/makenek", "test"]
    call(cmd, stdout=DEVNULL)
    return base

@delayed
def run(config):
    chdir(config["workdir"]) 
    cmd = ["/home/maxhutch/bin/nekmpi", "test", "{}".format(int(config["procs"]))]
    res = check_output(cmd)
    config['runstat'] = 1
    return config

@delayed
def analyze(config, res):
    chdir(config["workdir"])
    if config["restart"] == 0:
        first_frame = 1
        last_frame = config["num_steps"] / config["io_step"] + 1
    else:
        first_frame = config["restart"] + 1
        last_frame = first_frame + config["num_steps"] / config["io_step"] - 1
    cmd = ["/home/maxhutch/src/nek-analyze/load.py", "./test", 
            "-f", "{:d}".format(int(first_frame)), 
            "-e", "{:d}".format(int(last_frame))]
    rstat = call(cmd)
    config['analyzestat'] = rstat
    res.update(config)
    return res

@delayed
def report(configs):
    print(len(configs))
    return

@delayed
def update_config(base, diff):
    res = deepcopy(base)
    res.update(diff)
    return res

