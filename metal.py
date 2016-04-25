#!/home/maxhutch/anaconda3/bin/python3

from subprocess import call, check_output, DEVNULL

def genrun(d, u, path, name):
    cmd = ["/home/maxhutch/src/nek-tools/genrun/genrun.py", "-d",  d, "-u",  u, "--makenek={}".format(path), name]
    log = check_output(cmd)
    return log

def nekrun(name, procs):
    cmd = ["/home/maxhutch/bin/nekmpi", name, "{}".format(int(procs))]
    log = check_output(cmd)
    return log

def nekanalyze(name, start, end):
    cmd = ["/home/maxhutch/src/nek-analyze/load.py", "./{}".format(name), 
            "-f", "{:d}".format(int(start)), 
            "-e", "{:d}".format(int(end))]
    rstat = call(cmd, stdout=DEVNULL)
    return rstat

