from copy import deepcopy
from .tasks import prepare, update_config, run, analyze, prepare_
from dask.base import tokenize
from dask.delayed import delayed

from ..config import config as cfg

nekmpi_path = cfg.nekmpi
load_path   = cfg.load


def series(base, tusr, job_step = 0, job_time = 0.):
    if job_step > 0:
        njob = int((base["num_steps"]-1) / job_step) + 1
        base["io_step"] = min(base["io_step"], job_step)
        nio = int(job_step / base["io_step"])
    elif job_time > 0:
        njob = int(base["end_time"] / job_time + .5)
        nio = int(job_time / base["io_time"] + .5)
    else:
        njob = 1
        nio = 0 # not used

    restart = 0
    out_index = 0
    nres = max(3, base["torder"])
    end_time = job_time
    res = {}
    data = deepcopy(base)
    data["job_name"] = base["name"]
    data["job_time"] = job_time
    data = prepare(data, tusr)
    for i in range(njob):
        diff = {"restart": restart, "outind": out_index}
        if i == 0:
            restart   += 1
            out_index += nio + 1
        else:
            restart   += nres
            out_index += nio

        if job_step > 0:
            diff["num_steps"] = min(job_step, base["num_steps"] - i*job_step)
        if job_time > 0:
            diff["end_time"] = end_time
            end_time += job_time
        diff["job_name"] = "{}-{}".format(base["name"], i)
        config = update_config(data, diff)
        inp = prepare(config, tusr, make=False)
        data = run(inp, nekmpi_path)
        res = analyze(data, res)

    return res
