import numpy as np
from nekpy.tools.mesh import uniform_profile

def test_uniform():
    start = -1.0
    end = 2.0
    N = 9
    ref = np.linspace(start, end, N, endpoint=False)
    for i in range(N):
        assert abs(uniform_profile(i, N, start, end)[0] - ref[i]) < 1.0e-9
    assert abs(uniform_profile(2, N, start, end)[1] - (1.0 / 3.0)) < 1.0e-9 
