""" This file is part of the Gudhi Library - https://gudhi.inria.fr/ - which is released under MIT.
    See file LICENSE or go to https://gudhi.inria.fr/licensing/ for full license details.
    Author(s):       Vincent Rouvreau

    Copyright (C) 2016 Inria

    Modification(s):
      - 2025/04 Hannah Schreiber: Add tests to verify possibility of tensor input
      - YYYY/MM Author: Description of the modification
"""


from gudhi import EuclideanWitnessComplex, EuclideanStrongWitnessComplex


def test_empty_euclidean_witness_complex():
    euclidean_witness = EuclideanWitnessComplex()
    assert euclidean_witness._is_defined() == False


def test_witness_complex():
    point_cloud = [
        [1.0, 1.0],
        [7.0, 0.0],
        [4.0, 6.0],
        [9.0, 6.0],
        [0.0, 14.0],
        [2.0, 19.0],
        [9.0, 17.0],
    ]
    landmarks = [[1.0, 1.0], [7.0, 0.0], [4.0, 6.0]]
    euclidean_witness_complex = EuclideanWitnessComplex(
        landmarks=landmarks, witnesses=point_cloud
    )
    simplex_tree = euclidean_witness_complex.create_simplex_tree(max_alpha_square=4.1)

    assert landmarks[0] == euclidean_witness_complex.get_point(0)
    assert landmarks[1] == euclidean_witness_complex.get_point(1)
    assert landmarks[2] == euclidean_witness_complex.get_point(2)

    assert list(simplex_tree.get_filtration()) == [
        ([0], 0.0),
        ([1], 0.0),
        ([0, 1], 0.0),
        ([2], 0.0),
        ([0, 2], 0.0),
        ([1, 2], 0.0),
        ([0, 1, 2], 0.0),
    ]


def test_empty_euclidean_strong_witness_complex():
    euclidean_strong_witness = EuclideanStrongWitnessComplex()
    assert euclidean_strong_witness._is_defined() == False


def test_strong_witness_complex():
    point_cloud = [
        [1.0, 1.0],
        [7.0, 0.0],
        [4.0, 6.0],
        [9.0, 6.0],
        [0.0, 14.0],
        [2.0, 19.0],
        [9.0, 17.0],
    ]
    landmarks = [[1.0, 1.0], [7.0, 0.0], [4.0, 6.0]]
    euclidean_strong_witness_complex = EuclideanStrongWitnessComplex(
        landmarks=landmarks, witnesses=point_cloud
    )
    simplex_tree = euclidean_strong_witness_complex.create_simplex_tree(max_alpha_square=14.9)

    assert landmarks[0] == euclidean_strong_witness_complex.get_point(0)
    assert landmarks[1] == euclidean_strong_witness_complex.get_point(1)
    assert landmarks[2] == euclidean_strong_witness_complex.get_point(2)

    assert list(simplex_tree.get_filtration()) == [([0], 0.0), ([1], 0.0), ([2], 0.0)]

    simplex_tree = euclidean_strong_witness_complex.create_simplex_tree(max_alpha_square=100.0)

    assert list(simplex_tree.get_filtration()) == [
        ([0], 0.0),
        ([1], 0.0),
        ([2], 0.0),
        ([1, 2], 15.0),
        ([0, 2], 34.0),
        ([0, 1], 37.0),
        ([0, 1, 2], 37.0),
    ]


def test_tensors():
    try:
        import torch

        landmarks = (torch.rand((5, 2))).requires_grad_()
        witnesses = (torch.rand((5, 2))).requires_grad_()
        cplex = EuclideanWitnessComplex(landmarks=landmarks, witnesses=witnesses)
        cplex = EuclideanStrongWitnessComplex(landmarks=landmarks, witnesses=witnesses)
    except ImportError:
        pass

    try:
        import tensorflow as tf

        landmarks = tf.random.uniform(shape=[5, 2])
        witnesses = tf.random.uniform(shape=[5, 2])
        cplex = EuclideanWitnessComplex(landmarks=landmarks, witnesses=witnesses)
        cplex = EuclideanStrongWitnessComplex(landmarks=landmarks, witnesses=witnesses)
    except ImportError:
        pass
