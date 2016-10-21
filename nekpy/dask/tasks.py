import json
from os import chdir, makedirs
from dask.delayed import delayed, value
from copy import deepcopy
from ..config import config as cfg
from ..tools.genrun import genrun
from ..tools.genrun import default_config
from .metal import nekrun, nekanalyze
from hashlib import md5
#import .metal as metal
#import .dask import metal as metal

from importlib import import_module

metal = import_module(".metal", "nekpy.dask")

path = cfg.makenek
path_legacy = cfg.legacy
tools_path = cfg.tools

delayed = delayed(pure=True)

def configure(base, override, workdir):
    res = deepcopy(default_config)
    res.update(base)
    res.update(override)
    res["workdir"] = workdir
    if res["io_step"] == 0:
        res["io_step"] = 100000000
    if res["io_time"] == 0 and "end_time" in res:
        res["io_time"] = res["end_time"]
    return res 

def update_config(base, diff):
    res = deepcopy(base)
    res.update(diff)
    return res

def prepare_(base, tusr, make=True, legacy=False, dep=None):
    try:
        makedirs(base["workdir"])
    except OSError:
        pass
    chdir(base["workdir"]) 

    if legacy or "legacy" in base:
        genrun(base["job_name"], base, tusr, do_make = make, legacy=True, makenek=path_legacy, tools=tools_path)
    else:
        genrun(base["job_name"], base, tusr, do_make = make, legacy=False, makenek=path, tools=tools_path)

    return ""

def prepare(base, tusr, make=True, legacy=False, dep=None):
    name = "prepare-{}".format(base["job_name"]) 
    return delayed(prepare_)(base, tusr, make, legacy, dep, dask_key_name=name)

def run_(config, path="nekmpi", dep=None):
    chdir(config["workdir"]) 
    log = nekrun(config["job_name"], config["name"], config["procs"], path)
    with open("{}.stdout".format(config["job_name"]), "w") as f:
      f.write(log)

    return log

def run(config, path="nekmpi", dep=None):
    name = "run-{}".format(config["job_name"])
    return delayed(run_)(config, path, dep, dask_key_name=name)

def analyze_(config, res, dep=None):
    chdir(config["workdir"])
    if config["io_time"] > 0.:
        output_per_job = config["job_time"] / config["io_time"]
    else:
        output_per_job = config["num_steps"] / config["io_step"]
    if config["restart"] == 0:
        first_frame = 1
        last_frame = output_per_job + 1
    else:
        first_frame = config["outind"] + 1
        last_frame = first_frame + output_per_job - 1
    rstat = nekanalyze(config["name"], first_frame, last_frame)
    config['analyzestat'] = rstat
    res.update(config)
    return res

def analyze(config, res, dep=None):
    name = "analyze-{}".format(config["job_name"])
    return delayed(analyze_)(config, res, dep, dask_key_name=name)

