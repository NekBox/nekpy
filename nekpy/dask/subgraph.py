from copy import deepcopy
from .tasks import prepare, update_config, run, analyze

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
    data["job_name"] = base["name"]
    data = prepare(data, tusr)
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
        diff["job_name"] = "{}-{}".format(base["name"], i)
        config = update_config(data, diff)
        inp = prepare(config, tusr, make=False)
        data = run(inp)
        res = analyze(data, res)

    return res
