# matfuncutil
Containers for functional data in discrete and continuous forms.

## Installation

Clone the repository and install with the following commands:

    git clone https://github.com/petersbingham/matfuncutil
    cd matfuncutil
    python setup.py install
    
## Dependencies

Third party packages:
 - Matplotlib

Author (these will have their own dependencies):
 - [pynumwrap](https://github.com/petersbingham/pynumwrap)
 - [pynumutil](https://github.com/petersbingham/pynumutil)

## Overview

Computer representations of mathematical functions are typically in either continuous or discrete form. This package provides a convenient means to handle and switch between these different representations, as well as useful functionality, such as charting and serialisation of discrete data and root finding and discretisation of the continuous data. Scalars, vectors and matrices are supported.

For example we might have a set of data that we want to fit some function to, through a method such as least squares or polynomial fitting. This data will be in discrete form before the fit and continuous form after the fit (eg a polynomial). If we want to chart the fit it will first have to be converted to a discrete form again. 

### Discrete Containers

There are several forms for discrete data, all of which can be found in the `discrete` module. The common functionality is contained in `dBase`, which is an extension, and slight alteration, of the python dict type. Derived from base are `dSca`, `dVec` and `dMat` which provide containers mapping mpmath or numpy floats to either mpmath or numpy floats, vectors and matrices respectively.

As mentioned the discrete containers are like dicts. They map a float-like key (either python or mpmath) to either a float-like, vector-like or matrix-like value. The `__getitem__` function has been overridden and accepts either ints or float-likes. These are mapped to the actual float-like dict keys as follows:
 1. If the provided key is a float (either primitive python or mpmath) then it's directly mapped to the dictionary value in the standard manner.
 2. If an integer is provided as a key then this is used as an index to a sorted list of the dictionary keys. A tuple containing the dictionary key and it's corresponding quantity is returned.
 3. If a slice is provided then this is used to create a new dictionary obtained from applying the slice to a sorted list of the dictionary keys.

In addition, the helper function `get_slice_indices(self, startIndex, endIndex, num_points, from_end=False)` is provided to calculate the slice indices given a start key, end key and number of points. If the key is an int then refer to item 2 in the list above. If it's a float then item 1, with the additional functionality of returning the closest index if the provided float/s do not exist. An optional parameter, `from_end` is included to specify if the returned slice should be calculated relative to either the start or the end index. `get_slice_indices` could be useful, for example, when a fit routine requires a specified number of data at equal steps over an index range.

### Continuous Containers

The continuous module provides containers for the continuous representation. Similar to the discrete case there is a `cBase` from which is derived `cSca`, `cVec` and `cMat` containers. Each of these require a function reference for construction. In addition the  `cSympyPolySca` and `cSympyPolyMat` specialisations are available to handle containers of symbolic scalars and matrices.

Perhaps most usefully the `discretise` function will return a discrete container type providing all functionality described in the previous section. The discretised container will be lazily evaluated for efficiency; on the first call for a particular value it will be computed using the function reference and then cached into memory for any subsequent calls.

Other functionality is currently available to calculate determinants and find roots. When `find_roots` is called the object will either try and determine the roots using polynomial coefficients if available, or use a more general mechanism (TODO) otherwise.

The following illustrates a use case using the [`tisutil`](https://github.com/petersbingham/tisutil) package, which is an extension of `matfuncutil`:
 1. Obtain a `dKmat` container (derived from `dMat`) using the file reading package such as [`rfortmatreader`](https://github.com/petersbingham/ukrmolmatreader).
 2. Trim this to the required size using the `get_slice_indices` function.
 3. Pass this to some fitting routine such as [`parsmat`](https://github.com/petersbingham/parsmat).
 4. All being well it will return a continuous type container.
 5. We can then find the roots by calling `find_roots`.
 6. And\or create plots, convert to other quantities etc using the discrete interfaces on the return from the `discretise` function.

Also, we may not always start a fitting procedure with a discrete data set. For example [`twochanradialwell`]( https://github.com/petersbingham/twochanradialwell) returns a continuous type container. In this case we replace steps 1 and 2 above with:
 1. Obtain a continuous type container using some analytical solver or directly from the `twochanradialwell` (for example).
 2. Create an `dKmat` container of the appropriate range and length using the `discretise` function.

## Examples

The first example illustrates via a python shell session the indexing interface provided by the discrete containers.
```python
>>> from matfuncutil import *
>>> dsca = dSca({float(i):float(2.*i) for i in range(10,20)})
>>> dsca
{10.0: 20.0, 11.0: 22.0, 12.0: 24.0, 13.0: 26.0, 14.0: 28.0, 15.0: 30.0, 16.0: 32.0, 17.0: 34.0, 18.0: 36.0, 19.0: 38.0}
>>> dsca[0]
(10.0, 20.0)
>>> dsca[10.]
20.0
>>> slice,keys = dsca.get_slice_indices(0,6,3)
>>> slice
(0, 7, 3)
>>> keys
(10.0, 16.0)
>>> dsca2 = dsca[slice[0]:slice[1]:slice[2]]
>>> dsca2.sorted_values()
[10.0, 13.0, 16.0]
```

The second example is a simple python script showing conversion from a continuous container to a discrete container and subsequent plots. 
```python
import matfuncutil as mfu
import math

# Continuous container
csca = mfu.cSca(math.sin)
# Discretise to a discrete container
dsca = csca.discretise(0., 2.*math.pi, 200)

# Plot all points
dsca.plot()
# Reduce points using slice and plot
dsca[::20].plot()
```

This example shows the reduction of a discrete matrix container to a single element and then plotting of that element.
```python
import matfuncutil as mfu
import pynumwrap as nw

# Dummy set of matrices:
dmat = mfu.dMat({float(i):nw.matrix([[float(1.*i+1.),float(2.*i+1.)],[float(3.*i+1.),float(4.*i+1.)]]) for i in range(10,20)}, units="Test")
dmat.set_chart_title("Example Chart")

dmat.plot()                           # Plot all elements
dvec = dmat.create_reduced_dim(0)     # Convert to a vecs container containing rows
dvec.plot()                           # Plot all elements in row
dsca = dvec.create_reduced_dim(0)     # Convert to a scas container containing single element
dsca.plot()                           # Plot only a single element

# Or in short, to plot a single element:
dmat.create_reduced_dim(0).create_reduced_dim(0).plot()
```

## Container Descriptions

There are three optional strings in the containers: the `source_str`, the `hist_str` and the `chart_title`. The first of these identifies the container. The second is appended to on each operation; for example if the container is sliced then the newly created container's hist string will contain the slice info. Using these strings should allow reproduction of operations from the original data set if data is later serialised. The `chart_title` is used to title any plotted charts.
