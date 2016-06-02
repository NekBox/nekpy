nekpy
======

|Build Status| |Version Status| |Downloads|

Nek-related utilities in Python.

Tools
-------
`nekpy.tools` supports common pre- and post-processing tasks, such as populating `SIZE`, `rea`, and `usr` files and calling `makenek`. 
For the special case of single boxes, `nekpy.tools` can also generate meshes and map file.

Configuration
-------------

`nekpy` reads the paths to simulation and tools installations from the `~/.nekpy.json` file, which is created with default values if not present.


LICENSE
-------

MIT. See `License File <https://github.com/maxhutch/nekpy/blob/master/LICENSE>`__.

.. _documentation: http://dask.pydata.org/en/latest/
.. |Build Status| image:: https://travis-ci.org/maxhutch/nekpy.svg
   :target: https://travis-ci.org/maxhutch/nekpy
.. |Version Status| image:: https://img.shields.io/pypi/v/nekpy.svg
   :target: https://pypi.python.org/pypi/nekpy/
.. |Downloads| image:: https://img.shields.io/pypi/dm/nekpy.svg
   :target: https://pypi.python.org/pypi/nekpy/
