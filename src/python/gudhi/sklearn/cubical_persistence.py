# This file is part of the Gudhi Library - https://gudhi.inria.fr/ - which is released under MIT.
# See file LICENSE or go to https://gudhi.inria.fr/licensing/ for full license details.
# Author(s):       Vincent Rouvreau
#
# Copyright (C) 2021 Inria
#
# Modification(s):
#   - YYYY/MM Author: Description of the modification

__author__ = "Vincent Rouvreau"
__maintainer__ = ""
__copyright__ = "Copyright (C) 2021 Inria"
__license__ = "MIT"


import numpy as np
from typing import Union, Iterable, Literal, Optional
from sklearn.base import BaseEstimator, TransformerMixin
from joblib import Parallel, delayed

from .. import CubicalComplex
from .._pers_cub_low_dim import (
    _persistence_on_a_line,
    _persistence_on_rectangle_from_top_cells,
)


# Mermaid sequence diagram - https://mermaid-js.github.io/mermaid-live-editor/
# sequenceDiagram
#   participant USER
#   participant CP as CubicalPersistence
#   USER->>CP: fit_transform(X)
#   CP->>thread1: _tranform(X[0])
#   CP->>thread2: _tranform(X[1])
#   Note right of CP: ...
#   thread1->>CP: [array( H0(X[0]) ), array( H1(X[0]) )]
#   thread2->>CP: [array( H0(X[1]) ), array( H1(X[1]) )]
#   Note right of CP: ...
#   CP->>USER: [[array( H0(X[0]) ), array( H1(X[0]) )],<br/> [array( H0(X[1]) ), array( H1(X[1]) )],<br/> ...]


class CubicalPersistence(BaseEstimator, TransformerMixin):
    """
    This is a class for computing the persistence diagrams from a cubical complex.
    """

    def __init__(
        self,
        homology_dimensions: Union[int, Iterable[int]],
        input_type: Literal["top_dimensional_cells", "vertices"] = "top_dimensional_cells",
        homology_coeff_field: int = 11,
        min_persistence: float = 0.0,
        n_jobs: Optional[int] = None,
    ):
        """
        Constructor for the CubicalPersistence class.

        Parameters:
            homology_dimensions: The returned persistence diagrams dimension(s).
                Short circuit the use of :class:`~gudhi.representations.preprocessing.DimensionSelector` when only one
                dimension matters (in other words, when `homology_dimensions` is an int).
            input_type: 'top_dimensional_cells' if the filtration values passed to `transform()` are those of the
                top-dimensional cells, 'vertices' if they correspond to the vertices.
            homology_coeff_field: The homology coefficient field. Must be a prime number. Default value is 11.
            min_persistence: The minimum persistence value to take into account (strictly greater than
                `min_persistence`). Default value is `0.0`. Set `min_persistence` to `-1.0` to see all values.
            n_jobs: cf. https://joblib.readthedocs.io/en/latest/generated/joblib.Parallel.html
        """
        self.homology_dimensions = homology_dimensions
        self.input_type = input_type
        self.homology_coeff_field = homology_coeff_field
        self.min_persistence = min_persistence
        self.n_jobs = n_jobs

        # Done twice (in __init__ and fit), but exception is better the sooner
        dim_list = np.asarray(self.homology_dimensions, dtype=int)
        if dim_list.ndim not in [0, 1]:
            raise ValueError(f"Invalid dimension. Got {self.homology_dimensions=}, expected type=int|Iterable[int].")

    def fit(self, X, Y=None):
        """
        Fit the `CubicalPersistence` class in function of `homology_dimensions` type.
        """
        # Must be in the `fit` part, as `transform` should be const and as `__init__` is not called on a parallel grid
        # search for instance
        self._dim_list = np.asarray(self.homology_dimensions, dtype=int)
        self._unwrap = False
        if self._dim_list.ndim == 0:
            self._unwrap = True
            self._dim_list = self._dim_list.reshape(1)
        return self

    def __transform(self, cells):
        cells = np.asarray(cells)
        if len(cells.shape) == 1 and self.min_persistence >= 0:
            res = _persistence_on_a_line(cells)
            if self.min_persistence > 0:
                # It would be more efficient inside _persistence_on_a_line, but not worth it?
                res = res[res[:, 1] - res[:, 0] > self.min_persistence]
            # Wasteful if dim_list_ does not contain 0, but that seems unlikely.
            return [res if i == 0 else np.empty((0, 2)) for i in self._dim_list]

        if len(cells.shape) == 2 and self.input_type == "top_dimensional_cells" and self.min_persistence >= 0:
            if cells.size == 0:
                diags = [np.empty((0, 2)), np.empty((0, 2))]
            elif cells.shape[0] == 1 or cells.shape[1] == 1:
                diags = [_persistence_on_a_line(cells.reshape(-1)), np.empty((0, 2))]
            elif cells.shape[0] == 2:
                diags = [_persistence_on_a_line(cells.min(0)), np.empty((0, 2))]
            elif cells.shape[1] == 2:
                diags = [_persistence_on_a_line(cells.min(1)), np.empty((0, 2))]
            else:
                diags = _persistence_on_rectangle_from_top_cells(cells, self.min_persistence)
            return [diags[i] if i in (0, 1) else np.empty((0, 2)) for i in self._dim_list]

        if self.input_type == "top_dimensional_cells":
            cubical_complex = CubicalComplex(top_dimensional_cells=cells)
        elif self.input_type == "vertices":
            cubical_complex = CubicalComplex(vertices=cells)
        else:
            raise ValueError("input_type can only be 'top_dimensional_cells' or 'vertices'")
        cubical_complex.compute_persistence(
            homology_coeff_field=self.homology_coeff_field,
            min_persistence=self.min_persistence,
        )
        return [cubical_complex.persistence_intervals_in_dimension(dim) for dim in self._dim_list]

    def transform(self, X, Y=None):
        """Compute all the cubical complexes and their associated persistence diagrams.

        :param X: Filtration values of the top-dimensional cells or vertices for each complex.
        :type X: list of array-like

        :return: Persistence diagrams in the format:

              - If `homology_dimensions` was set to `n`: `[array( Hn(X[0]) ), array( Hn(X[1]) ), ...]`
              - If `homology_dimensions` was set to `[i, j]`:
                `[[array( Hi(X[0]) ), array( Hj(X[0]) )], [array( Hi(X[1]) ), array( Hj(X[1]) )], ...]`
        :rtype: list of (,2) array_like or list of list of (,2) array_like
        """
        # threads is preferred as cubical construction and persistence computation releases the GIL
        res = Parallel(n_jobs=self.n_jobs, prefer="threads")(delayed(self.__transform)(cells) for cells in X)
        # cf. `fit`
        if self._unwrap:
            res = [d[0] for d in res]
        return res
