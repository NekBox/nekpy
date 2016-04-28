from nekpy.dask.utils import outer_product

def test_outer_product():
    opts = {"foo": ["bar",], "spam": ["eggs", "spam"]}
    outer = list(outer_product(opts))
    assert len(outer) == 2
    assert outer[0]["spam"] != outer[1]["spam"]
