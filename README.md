# scatteringutil
Utilities related to the scattering quantities.

## Installation

Clone the repository and install with the following commands:

    git clone https://github.com/petersbingham/scatteringutil.git
    cd scatteringutil
    python setup.py install
    
## Dependencies


## Overview

In time-independent scattering there are several means with which to characterise the collision; the S-matrix, K-matrix, T-matrix and the eigenphase shift being typical. From these we can derive quantities such as the cross-section. Computationally the characterisations can be quantified either as discrete sets of data, for example from numerical scattering calculations, or as a continuous function, for example an analytically obtained solution to a scattering problem or from fitting to the discrete data.

This package provides a convenient means to handle and switch between these different representations, as well as provide useful functionality, such as charting and serialisation of discrete data and root finding and discretisation of the continuous data.

There are then two main categorisations provided: the discrete form and the continuous form. The following sections describe these and how to convert from one to the other.

## Usage

### Discrete
We start with a couple of examples and then details follow. A simple example, showing how to plot a cross section in eVs, starting from a set of S-matrices:
```python
smats = somepackage.readSmats()             # Obtain set of S-matrices
reduced_smats = smats[100:500:10]           # Reduce to 80 points between 100 and 500
reduced_smats_eV = smats.convertUnits(eVs)  # Convert to eVs
XS_vals = reduced_smats_eV.getXS()          # Calculate XS
XS_vals.plot()                              # Create MATPLOTLIB plot
```
We can also plot all elements, rows or single elements of the matrices:
```python
smats = somepackage.readSmats()             # Obtain set of S-matrices
smats.plot()                                # Plot all elements
smats_rows = smats.getRow(0)                # Convert to a vecs container containing rows
smats_rows.plot()                           # Plot all elements in row
smats_eles = smats.getElement(0)            # Convert to a vals container containing single element
smats_eles.plot()                           # Plot only a single element

# Or in short, to plot a single element:
smats.getRow(0).getElement(0).plot()
```
Finally, an example showing how to convert from K-matrices to S-matrices and how to save and load a specified number of these to file:
```python
import scatteringutil as su
kmats = somepackage.readKmats()             # Obtain set of K-matrices
smats = kmats.toSMats()
with open("Output.txt", "w") as text_file:
    text_file.write(str(smats))             # Write the data to file
# ...
# Later on read it back again and use to initialise container:
with open("Output.txt", "r") as file:
    content = file.read()
smats = su.discrete.Smats(content)          # Initialise the container using the serialised data.
```

There are several forms for discrete data, all of which can be found in the `discrete` module. The common functionality is contained in `base`, which is an extension, and slight alteration, of the python `dict` type. It is assumed that the keys of this dictionary are the scattering energies and the corresponding values the mapped quantities (eg S-matrices). Derived from `base` are `vals`, `vecs` and `mats` which provide containers mapping energy to either mpmath or numpy primitives, vectors and matrices respectively. Finally, derived from `mats` are `Smats`, `Kmats` and `Tmats`. Each of these scattering related containers provides the means to move from one to another, as well as the ability to transform into `vecs` container or various `vals` containers, such as total-cross-section and eigenphase sums. A discrete container can be built in code using the common dictionary interface. It can also be returned from other modules, such as the `rfortmatreader`. 

The discrete container is indexed using the following rules:
 * If an integer is provided then this is used as an index to a sorted list of the energy. A tuple containing this energy and it's corresponding quantity is returned.
 * If a float (either primitive python or mpmath) is provided then it's associated quantity is returned.
 * If a slice is provided then this is used to create a dictionary based on energies and associated quantities obtained from applying the slice to a sorted list of the energies.

In addition, the helper function `base.calculateReductionIndices(self, startIndex, endIndex, numPoints, fromEnd=False)` is provided to calculate the slice indices given a start index, end index and number of points. An optional parameter is included to specify if this should be calculated from either the start or the end index. This is useful for example when a fit routine requires a specified number of data at equal steps over an indice range.  Here is a console demo of this functionality:

```python
>>> from scatteringutil.discrete import *
>>> v = vals({float(i):float(2.*i) for i in range(10,20)})
>>> v
{10.0: 20.0, 11.0: 22.0, 12.0: 24.0, 13.0: 26.0, 14.0: 28.0, 15.0: 30.0, 16.0: 32.0, 17.0: 34.0, 18.0: 36.0, 19.0: 38.0}
>>> v[0]
(10.0, 20.0)
>>> v[10.]
20.0
>>> slice,energies = v.calculateReductionIndices(0,6,3)
>>> slice
(0, 7, 3)
>>> energies
(10.0, 16.0)
>>> v2 = v[slice[0]:slice[1]:slice[2]]
>>> v2.sortedEnergies()
[10.0, 13.0, 16.0]
```

### Continuous
The continuous module provides functionality relating to the scattering quantities in continuous form, such as the `getCoefficients` and `getRoots` functions. When `getRoots` is called the object will either try and determine the roots using polynomial coefficients if available, or use a more general mechanism otherwise.

Perhaps most usefully the `discretise` function will return a `discrete` container type providing all functionality described in the previous section. In essense we can for example:
 1. Obtain a `Smats` container using some file reading package such as `rfortmatreader`.
 2. Trim this to the required size using the slicing functionality.
 3. Pass this to some fitting routine such as `parSmat`.
 4. All being well it will return a `continuous` type container.
 5. We can then find the roots by calling `getRoots`.
 6. And\or create plots, convert to other quantities etc using the `discrete` interfaces on the return from the `discretise` function.

Also, we may not always start a fitting procedure with a discrete data set. For example `radialwellsolver` returns a `continuous` type container. In this case we replace steps 1, and 2, above with:
 1. Obtain a `continuous` type container using some analytical solver or directly from the `radialwellsolver` (for example).
 2. Create an `Smats` container of the appropriate range and length using the `discretise` function.
 
