#!/home/maxhutch/anaconda3/bin/python3

from subprocess import call, check_output, DEVNULL

genrun_path = "/home/maxhutch/src/nek-tools/genrun/genrun.py"
nekmpi_path = "/home/maxhutch/bin/nekmpi"
load_path   = "/home/maxhutch/src/nek-analyze/load.py"

def genrun(d, u, path, name, make=True):
    cmd = [genrun_path, "-d",  d, "-u",  u, "--makenek={}".format(path), name]
    if not make:
        cmd.append("--no-make")
    log = check_output(cmd)
    return log

def nekrun(name, job_name, procs):
    cmd = [nekmpi_path, name, "{}".format(int(procs)), job_name]
    log = check_output(cmd).decode()
    return log

def nekanalyze(name, start, end):
    cmd = [load_path, "./{}".format(name), 
            "-f", "{:d}".format(int(start)), 
            "-e", "{:d}".format(int(end)),
            "--single_pos"]
    rstat = call(cmd, stdout=DEVNULL)
    return rstat

