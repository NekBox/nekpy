from dask.callbacks import Callback
from os import getcwd, remove
from os.path import join, exists
from dask.diagnostics import ProgressBar, Profiler, ResourceProfiler, CacheProfiler
#from dask.multiprocessing import get
from dask.dot import dot_graph
from dask.async import get_sync as get
from dask import compute
import toolz
import json

class NekCallback(Callback):
    def __init__(self, case):
        self.case = case
        self.cwd  = getcwd()
        self.cache = {}
        if exists(join(self.cwd, "HALT")):
            remove(join(self.cwd, "HALT"))

    def _posttask(self, key, result, dsk, state, id):
        self.cache.update(state['cache'])
        with open(join(self.cwd, "{}.cache".format(self.case["prefix"])), "w") as f:
            json.dump(self.cache, f)

        if exists(join(self.cwd, "HALT")):
            for k in state['ready']:
                state['cache'][k] = None
            for k in state['waiting']:
                state['cache'][k] = None
            state['ready'] = []
            state['waiting'] = []

        return

def run_all(values, base):
    full_dask = toolz.merge(val.dask for val in values)
    full_keys = [val._key for val in values]

    cache = {}
    if exists("{}.cache".format(base["prefix"])):
        with open("{}.cache".format(base["prefix"]), "r") as f:
            cache = json.load(f)

    full_dask.update(cache)
    dot_graph(full_dask)

    with ProgressBar(), NekCallback(base), Profiler() as prof, ResourceProfiler(dt=1.0) as rprof:
        res = get(full_dask, full_keys, cache=cache)

    return res
