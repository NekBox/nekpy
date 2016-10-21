from itertools import product

def outer_product(options):
    return (dict(zip(options, x)) for x in product(*options.values()))

def work_name(prefix, options):
    res = prefix
    for key, val in sorted(options.items()):
        res = res + "_{}_{}".format(key[0:2], val)
    return res
