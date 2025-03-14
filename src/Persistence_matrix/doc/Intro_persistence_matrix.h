/*    This file is part of the Gudhi Library - https://gudhi.inria.fr/ - which is released under MIT.
 *    See file LICENSE or go to https://gudhi.inria.fr/licensing/ for full license details.
 *    Author(s):       Hannah Schreiber
 *
 *    Copyright (C) 2024 Inria
 *
 *    Modification(s):
 *      - YYYY/MM Author: Description of the modification
 */

#ifndef DOC_PERSISTENCE_MATRIX_INTRO_PERSISTENCE_MATRIX_H_
#define DOC_PERSISTENCE_MATRIX_INTRO_PERSISTENCE_MATRIX_H_

// needs namespace for Doxygen to link on classes
namespace Gudhi {
namespace persistence_matrix {

/** \defgroup persistence_matrix Persistence Matrix
 * @{
 * \author    Hannah Schreiber
 *
 * \section matrixintro Persistence Matrix
 *
 * The module provides a data structure for matrices, in particular thought for matrices representing filtered complexes
 * and used as backend for persistence algorithms, such at persistent homology, @ref persistent_cohomology,
 * or zigzag @cite zigzag.
 *
 * The structure is entirely accessed via the class @ref Matrix and it provides several functionalities which can
 * be enabled or disabled through a template argument following the @ref PersistenceMatrixOptions concept.
 * The main functionalities are:
 * @li column and row access,
 * @li column addition and scalar multiplication,
 * @li removal of maximal cells while maintaining a valid reduced boundary matrix or compatible chain complex base
 * and a valid barcode with respect to the new filtration,
 * @li computation of persistent homology (but note that if the barcode is your only necessity, using the
 * @ref persistent_cohomology module is often more performant),
 * @li computation of representative cycles for the cycle classes,
 * @li swapping of two consecutive cells in a filtration (cf. vineyards @cite vineyards) while maintaining a valid
 * reduced boundary matrix or compatible chain complex base and a valid barcode with respect to the new filtration,
 * 
 * \note Matrix API is in a beta version and may change in incompatible ways in the near future.
 *
 * \subsection matrixexamples Examples
 * 
 * Here is a list of examples using the module:
 * \li \gudhi_example_link{Persistence_matrix,example_representative_cycles_from_matrix.cpp} - A simple example on how to
 * use the matrix to compute representative cycles.
 *
 * \li \gudhi_example_link{Persistence_matrix,example_simplex_tree_to_matrix.cpp} - A simplex example on how to build
 * a the different matrices from a simplex tree.
 * 
 * @}
 */
}  // namespace persistence_matrix
}  // namespace Gudhi

#endif  // DOC_PERSISTENCE_MATRIX_INTRO_PERSISTENCE_MATRIX_H_
