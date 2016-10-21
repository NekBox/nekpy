from copy import deepcopy
from .tasks import prepare, update_config, run, analyze, prepare_
from dask.base import tokenize
from dask.delayed import delayed
from math import ceil

from ..config import config as cfg

nekmpi_path = cfg.nekmpi
load_path   = cfg.load


def series(base_in, tusr, job_step = 0, job_time = 0.):
    base = deepcopy(base_in)
    if job_step > 0:
        njob = int((base["num_steps"]-1) / job_step) + 1
        base["io_step"] = min(base["io_step"], job_step)
        nio = int(job_step / base["io_step"])
    elif job_time > 0:
        njob = int(ceil(base["end_time"] / job_time))
        nio = int(ceil(job_time / base["io_time"]))
    else:
        njob = 1
        nio = 0 # not used

    restart = 0
    out_index = 0
    nres = max(3, base["torder"])
    end_time = job_time
    res = {}
    data = deepcopy(base)
    base["job_name"] = base["name"]
    base["job_time"] = job_time
    data = prepare(base, tusr)
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
        config = update_config(base, diff)
        inp = prepare(config, tusr, make=False, dep=data)
        data = run(config, nekmpi_path, dep=inp)
        res = analyze(config, res, dep=data)

    return res
