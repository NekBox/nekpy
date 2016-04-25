import json
from os import chdir, makedirs
from dask.imperative import delayed, value
from copy import deepcopy
from metal import genrun, nekrun, nekanalyze

makenek = "/home/maxhutch/src/NekBox/makenek"

delayed = delayed(pure=True)

def configure(base, override, workdir):
    res = deepcopy(base)
    res = dict(list(res.items()) + list(override.items()))
    res["workdir"] = workdir
    if res["io_step"] == 0:
        res["io_step"] = 100000000
    return res 

@delayed
def prepare(base, tusr, make=True):
    try:
        makedirs(base["workdir"])
    except OSError:
        pass
    chdir(base["workdir"]) 
    with open("cf.json", "w") as f:
        json.dump(base, f, indent=2)

    with open("cf.tusr", "w") as f:
        f.write(tusr)

    genrun("cf.json", "cf.tusr", makenek, base["job_name"], make=make)
    return base

@delayed
def run(config):
    chdir(config["workdir"]) 
    log = nekrun(config["job_name"], config["name"], config["procs"])
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
    rstat = nekanalyze(config["name"], first_frame, last_frame)
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

