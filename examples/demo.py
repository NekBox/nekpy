#!/home/maxhutch/anaconda3/bin/python3

import json
from os import getcwd
#from dask.multiprocessing import get
from dask.dot import dot_graph
from dask.async import get_sync as get
from nekpy.dask.subgraph import series
from nekpy.dask.utils import outer_product, work_name
from nekpy.dask import run_all
from nekpy.dask.tasks import configure
from dask import compute
import toolz


from sys import argv
with open(argv[1], "r") as f:
    base = json.load(f)

with open(argv[2], "r") as f:
    sweeps = json.load(f)

with open(argv[3], "r") as f:
    tusr = f.read()

base["prefix"] = sweeps["prefix"]
del sweeps["prefix"]

overrides = list(outer_product(sweeps))
for ov in overrides:
    ov["name"] = work_name(base["prefix"], ov)


from os.path import join
workdirs = [join(getcwd(), x["name"]) for x in overrides]
configs = [configure(base, override, workdir) for override, workdir in zip(overrides, workdirs)]
res = [series(config, tusr, job_step = 25) for config in configs]
#final = report(res)

final = run_all(res, base)

from dask.diagnostics import visualize
#visualize([prof, rprof])

