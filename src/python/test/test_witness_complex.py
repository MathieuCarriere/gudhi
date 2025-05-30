""" This file is part of the Gudhi Library - https://gudhi.inria.fr/ - which is released under MIT.
    See file LICENSE or go to https://gudhi.inria.fr/licensing/ for full license details.
    Author(s):       Vincent Rouvreau

    Copyright (C) 2016 Inria

    Modification(s):
      - 2025/04 Hannah Schreiber: Add tests to verify possibility of tensor input
      - YYYY/MM Author: Description of the modification
"""


from gudhi import WitnessComplex, StrongWitnessComplex, SimplexTree


def test_empty_witness_complex():
    witness = WitnessComplex()
    assert witness._is_defined() == False


def test_witness_complex():
    nearest_landmark_table = [
        [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]],
        [[1, 0], [2, 1], [3, 2], [4, 3], [0, 4]],
        [[2, 0], [3, 1], [4, 2], [0, 3], [1, 4]],
        [[3, 0], [4, 1], [0, 2], [1, 3], [2, 4]],
        [[4, 0], [0, 1], [1, 2], [2, 3], [3, 4]],
    ]

    witness_complex = WitnessComplex(nearest_landmark_table=nearest_landmark_table)
    simplex_tree = witness_complex.create_simplex_tree(max_alpha_square=4.1)
    assert simplex_tree.num_vertices() == 5
    assert simplex_tree.num_simplices() == 31
    simplex_tree = witness_complex.create_simplex_tree(max_alpha_square=4.1, limit_dimension=2)
    assert simplex_tree.num_vertices() == 5
    assert simplex_tree.num_simplices() == 25


def test_strong_witness_complex():
    nearest_landmark_table = [
        [[0, 0], [1, 1], [2, 2], [3, 3], [4, 4]],
        [[1, 0], [2, 1], [3, 2], [4, 3], [0, 4]],
        [[2, 0], [3, 1], [4, 2], [0, 3], [1, 4]],
        [[3, 0], [4, 1], [0, 2], [1, 3], [2, 4]],
        [[4, 0], [0, 1], [1, 2], [2, 3], [3, 4]],
    ]

    strong_witness_complex = StrongWitnessComplex(
        nearest_landmark_table=nearest_landmark_table
    )
    simplex_tree = strong_witness_complex.create_simplex_tree(max_alpha_square=4.1)
    assert simplex_tree.num_vertices() == 5
    assert simplex_tree.num_simplices() == 31
    simplex_tree = strong_witness_complex.create_simplex_tree(
        max_alpha_square=4.1, limit_dimension=2
    )
    assert simplex_tree.num_vertices() == 5
    assert simplex_tree.num_simplices() == 25

def test_tensors():
    try:
        import torch

        nearest_landmark_table = (torch.rand((5, 5, 2))).requires_grad_()
        cplex = StrongWitnessComplex(nearest_landmark_table)
        cplex = WitnessComplex(nearest_landmark_table)
    except ImportError:
        pass

    try:
        import tensorflow as tf

        nearest_landmark_table = tf.random.uniform(shape=[5, 5, 2])
        cplex = StrongWitnessComplex(nearest_landmark_table)
        cplex = WitnessComplex(nearest_landmark_table)
    except ImportError:
        pass
