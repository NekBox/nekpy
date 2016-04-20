#!/home/maxhutch/anaconda3/bin/python3

import json
from os import chdir, makedirs
from dask.imperative import delayed, value
from subprocess import call
from dask.dot import dot_graph
from dask.multiprocessing import get

@delayed
def prepare(base, tusr, override, workdir):
    try:
        makedirs(workdir)
    except OSError:
        pass
    chdir(workdir) 
    config = dict(list(base.items()) + list(override.items()))
    with open("cf.json", "w") as f:
        json.dump(config, f, indent=2)

    cmd = ["/home/maxhutch/src/nek-tools/genrun/genrun.py", "-d",  "./cf.json", "-u",  "{}".format(tusr), "--makenek=/home/maxhutch/src/NekBox/makenek", "test"]
    call(cmd)
    return config

@delayed
def run(config, workdir):
    chdir(workdir) 
    cmd = ["/home/maxhutch/bin/nekmpi", "test", "{}".format(int(config["procs"]))]
    res = call(cmd)
    config['runstat'] = res
    return config

@delayed
def analyze(config, workdir):
    chdir(workdir)
    cmd = ["/home/maxhutch/src/nek-analyze/load.py", "./test", "-f", "1", "-e", "2"]
    res = call(cmd)
    config['analyzestat'] = res
    return config

@delayed
def report(configs):
    print(len(configs))
    return

from sys import argv
with open(argv[1], "r") as f:
    base = json.load(f)

tusr = argv[2]

courants = [0.1, 0.2, 0.3, 0.4]
#courants = [0.1]
overrides = [{"courant": x} for x in courants]
workdirs = ["/home/maxhutch/src/nek_dask/test_{}".format(x) for x in courants]
configs = [prepare(base, tusr, override, workdir) for override, workdir in zip(overrides, workdirs)]
runs = [run(config, workdir) for config, workdir in zip(configs, workdirs)]
res = [analyze(data, workdir) for data, workdir in zip(runs, workdirs)]
final = report(res)

dot_graph(final.dask)
final.compute(get=get)

