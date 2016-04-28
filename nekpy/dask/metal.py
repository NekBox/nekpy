#!/home/maxhutch/anaconda3/bin/python3

from subprocess import call, check_output, DEVNULL
from ..config import config as cfg

def nekrun(name, job_name, procs):
    cmd = [cfg.nekmpi, name, "{}".format(int(procs)), job_name]
    log = check_output(cmd).decode()
    return log

def nekanalyze(name, start, end):
    cmd = [cfg.load, "./{}".format(name), 
            "-f", "{:d}".format(int(start)), 
            "-e", "{:d}".format(int(end)),
            "--single_pos"]
    rstat = call(cmd, stdout=DEVNULL)
    return rstat

