#!/home/maxhutch/anaconda3/bin/python3

import json
from os import chdir, makedirs
from dask.imperative import delayed, value
from subprocess import call
from dask.dot import dot_graph
from dask.multiprocessing import get
from copy import deepcopy
from tasks import *

from itertools import product

def outer_product(options):
    return (dict(zip(options, x)) for x in product(*options.values()))

def work_name(options):
    res = "/home/maxhutch/src/nek_dask/test"
    for key, val in options.items():
        res = res + "_{}_{}".format(key, val)
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
    res = {}
    data = deepcopy(base)
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
        config = update_config(data, diff)
        inp = prepare(config, tusr)
        data = run(inp)
        res = analyze(data, res)

    return res

from sys import argv
with open(argv[1], "r") as f:
    base = json.load(f)

with open(argv[2], "r") as f:
    sweeps = json.load(f)

tusr = argv[3]

overrides = list(outer_product(sweeps))
workdirs = [work_name(x) for x in overrides]
configs = [configure(base, override, workdir) for override, workdir in zip(overrides, workdirs)]
res = [series(config, tusr, job_step = 25) for config in configs]
final = report(res)

dot_graph(final.dask)
from dask.diagnostics import ProgressBar, Profiler, ResourceProfiler, CacheProfiler
with ProgressBar(), Profiler() as prof, ResourceProfiler(dt=1.0) as rprof:
    final.compute(get=get)

from dask.diagnostics import visualize
#visualize([prof, rprof])

