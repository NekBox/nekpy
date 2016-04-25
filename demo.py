#!/home/maxhutch/anaconda3/bin/python3

import json
from os import chdir, makedirs
from dask.imperative import delayed, value
from subprocess import call
from dask.dot import dot_graph
from dask.multiprocessing import get
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
    call(cmd)
    return base

@delayed
def run(config):
    chdir(config["workdir"]) 
    cmd = ["/home/maxhutch/bin/nekmpi", "test", "{}".format(int(config["procs"]))]
    res = call(cmd)
    config['runstat'] = res
    return config

@delayed
def analyze(config):
    chdir(config["workdir"])
    cmd = ["/home/maxhutch/src/nek-analyze/load.py", "./test", "-f", "1", "-e", "2"]
    res = call(cmd)
    config['analyzestat'] = res
    return config

@delayed
def report(configs):
    print(len(configs))
    return

@delayed
def update_config(base, diff):
    res = deepcopy(base)
    res.update(diff)
    return res

def series(base, tusr, job_step = 0, job_time = 0.):
    if job_step > 0:
        njob = int(base["num_steps"] / job_step)
        base["io_step"] = min(base["io_step"], job_step)
        nio = int(job_step / base["io_step"])
    elif jobs_time > 0:
        njob = int(base["end_time"] / job_time + .5)
        nio = int(job_time / base["io_time"] + .5)

    restart = 0
    end_time = job_time
    for i in range(njob):
        diff = {"restart": restart}
        restart += nio
        if i == 0:
            restart += 1

        if job_step > 0:
            diff["num_steps"] = job_step
        if job_time > 0:
            diff["end_time"] = end_time
            end_time += job_time
        config = update_config(base, diff)
        config = prepare(config, tusr)
        base = run(config)

    return base

from sys import argv
with open(argv[1], "r") as f:
    base = json.load(f)

tusr = argv[2]

courants = [0.3, 0.4]
#courants = [0.1]
overrides = [{"courant": x} for x in courants]
workdirs = ["/home/maxhutch/src/nek_dask/test_{}".format(x) for x in courants]
configs = [configure(base, override, workdir) for override, workdir in zip(overrides, workdirs)]
# = [prepare(base, tusr, override, workdir) for override, workdir in zip(overrides, workdirs)]
runs = [series(config, tusr, job_step = 50) for config in configs]
res = [analyze(data) for data in runs]
final = report(res)

dot_graph(final.dask)
final.compute(get=get)

