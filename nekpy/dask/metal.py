#!/home/maxhutch/anaconda3/bin/python3

from subprocess import call, check_output, DEVNULL
from ..config import config as cfg

nekmpi_path = cfg.nekmpi
load_path   = cfg.load

def nekrun(name, series_name, procs, path="nekmpi"):
    cmd = [path, name, "{}".format(int(procs)), series_name]
    log = check_output(cmd).decode()
    return log

def nekanalyze(name, start, end):
    cmd = [load_path, "./{}".format(name), 
            "-f", "{:d}".format(int(start)), 
            "-e", "{:d}".format(int(end)),
            "--single_pos"]
    rstat = call(cmd, stdout=DEVNULL)
    return rstat

