#!/usr/bin/env python

""" This file is part of the Gudhi Library - https://gudhi.inria.fr/ - which is released under MIT.
    See file LICENSE or go to https://gudhi.inria.fr/licensing/ for full license details.
    Author(s):       Hind Montassif

    Copyright (C) 2021 Inria

    Modification(s):
      - YYYY/MM Author: Description of the modification
"""

# Because of AlphaComplex - datasets.generators.points.sphere is LGPL v3
__license__ = "GPL v3"


from gudhi.datasets.generators import points
from gudhi import AlphaComplex


print("#####################################################################")
print("AlphaComplex creation from generated points on sphere")


gen_points = points.sphere(n_samples=50, ambient_dim=2, radius=1, sample="random")

# Create an alpha complex
alpha_complex = AlphaComplex(points=gen_points)
simplex_tree = alpha_complex.create_simplex_tree()

result_str = (
    "Alpha complex is of dimension "
    + repr(simplex_tree.dimension())
    + " - "
    + repr(simplex_tree.num_simplices())
    + " simplices - "
    + repr(simplex_tree.num_vertices())
    + " vertices."
)
print(result_str)
