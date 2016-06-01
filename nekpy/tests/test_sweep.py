import json
from os import getcwd
from nekpy.dask.subgraph import series
from nekpy.dask.utils import outer_product, work_name
from nekpy.dask import run_all
from nekpy.dask.tasks import configure
from os.path import join, dirname

def test_sweep():

    with open(join(dirname(__file__), "LST.json"), "r") as f:
        base = json.load(f)

    with open(join(dirname(__file__), "LST.sweep"), "r") as f:
        sweeps = json.load(f)

    with open(join(dirname(__file__), "LST.tusr"), "r") as f:
        tusr = f.read()

    base["prefix"] = sweeps["prefix"]
    del sweeps["prefix"]

    overrides = list(outer_product(sweeps))
    for ov in overrides:
        ov["name"] = work_name(base["prefix"], ov)

    workdirs = [join(getcwd(), "s", x["name"]) for x in overrides]
    configs = [configure(base, override, workdir) for override, workdir in zip(overrides, workdirs)]
    res = [series(config, tusr, job_step = 25) for config in configs]

    final = run_all(res, base)

