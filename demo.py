#!/home/maxhutch/anaconda3/bin/python3

import json
from os import chdir, makedirs, getcwd
from dask.imperative import delayed, value
from subprocess import call
from dask.dot import dot_graph
from dask.multiprocessing import get

@delayed
def prepare(base, tusr, override, workdir):
  cwd = getcwd()
  try:
    makedirs(workdir)
  except OSError:
    pass
  chdir(workdir) 
  config = dict(list(base.items()) + list(override.items()))
  with open("cf.json", "w") as f:
    json.dump(config, f, indent=2)

  cmd = ["/home/maxhutch/src/nek-tools/genrun/genrun.py", "-d",  "./cf.json", "-u",  "{}".format(tusr), "--makenek=/home/maxhutch/src/NekBox/makenek", "test"]
  print(cmd)
  call(cmd)
  chdir(cwd)
  return config

@delayed
def run(config, workdir):
  cwd = getcwd()
  chdir(workdir) 
  cmd = ["/home/maxhutch/bin/nekmpi", "test", "{}".format(int(config["procs"]))]
  print(cmd)
  res = call(cmd)
  chdir(cwd)
  return res

@delayed
def report(rets):
  print(rets)
  return

from sys import argv
with open(argv[1], "r") as f:
  base = json.load(f)

tusr = argv[2]

courants = [0.1, 0.2]
overrides = [{"courant": x} for x in courants]
workdirs = ["/home/maxhutch/src/nek_dask/test_{}".format(x) for x in courants]
d = {
    'c0' :  (prepare, base, tusr, overrides[0], workdirs[0]),
    'c1' :  (prepare, base, tusr, overrides[1], workdirs[1]),
    'r0' :  (run, 'c0', workdirs[0]),
    'r1' :  (run, 'c1', workdirs[1]),
    'd0' :  (report, ['r0', 'r1'])
}


configs = [prepare(base, tusr, override, workdir) for override, workdir in zip(overrides, workdirs)]
runs = [run(config, workdir) for config, workdir in zip(configs, workdirs)]
res = report(runs)
dot_graph(res.dask)
res.compute()

#get(d, 'd0')

