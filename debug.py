#!/usr/bin/env python3

import json
from tasks import *
with open("./examples/LST.json", "r") as f:
    base = json.load(f)
with open("./examples/LST_f90.tusr", "r") as f:
    tusr = f.read()
print(prepare(base, tusr)._key)

