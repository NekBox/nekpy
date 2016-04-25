#!/home/maxhutch/anaconda3/bin/python3

import json
from os import chdir, makedirs
from dask.imperative import delayed, value
from subprocess import call
from dask.dot import dot_graph
from dask.multiprocessing import get
from copy import deepcopy
from tasks import *

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

