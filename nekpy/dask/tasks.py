import json
from os import chdir, makedirs
from dask.delayed import delayed, value
from copy import deepcopy
from ..config import config as cfg
from ..tools.genrun import genrun

from importlib import import_module
metal = import_module(".metal", "nekpy.dask")

path = cfg.makenek

delayed = delayed(pure=True)

def configure(base, override, workdir):
    res = deepcopy(base)
    res.update(override)
    res["workdir"] = workdir
    if res["io_step"] == 0:
        res["io_step"] = 100000000
    if res["io_time"] == 0 and "end_time" in res:
        res["io_time"] = res["end_time"]
    return res 

@delayed
def prepare(base, tusr, make=True):
    try:
        makedirs(base["workdir"])
    except OSError:
        pass
    chdir(base["workdir"]) 

    genrun(base["job_name"], base, tusr, do_make = make, makenek=path)
    return base

@delayed
def run(config):
    chdir(config["workdir"]) 
    log = metal.nekrun(config["job_name"], config["name"], config["procs"])
    with open("{}.stdout".format(config["job_name"]), "w") as f:
      f.write(log)
    config['runstat'] = 1
    return config

@delayed
def analyze(config, res):
    chdir(config["workdir"])
    if config["io_time"] > 0.:
        output_per_job = config["job_time"] / config["io_time"]
    else:
        output_per_job = config["num_steps"] / config["io_step"]
    if config["restart"] == 0:
        first_frame = 1
        last_frame = output_per_job + 1
    else:
        first_frame = config["restart"] + 1
        last_frame = first_frame + output_per_job - 1
    rstat = metal.nekanalyze(config["name"], first_frame, last_frame)
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

