#ifndef CGSOLVER_HPP
#define CGSOLVER_HPP

#include <vector>

#include "matvecops.hpp"
#include "sparse.hpp"

/* Function that implements the CG algorithm for a linear system
 *
 * Ax = b
 *
 * where A is in CSR format.  The starting guess for the solution
 * is provided in x, and the solver runs a maximum number of iterations
 * equal to the size of the linear system.  Function returns the
 * number of iterations to converge the solution to the specified
 * tolerance, or -1 if the solver did not converge.
 */

int CGSolver(SparseMatrix &A,
             const std::vector<double> &b,
             std::vector<double> &x,
             double              tol,
             std::string soln_prefix,
             unsigned int ncols, unsigned int nrows);

void write_soln(std::string soln_prefix, const std::vector<double> &x, int niter,
    unsigned int ncols, unsigned int nrows, const std::vector<double> &b);
#endif /* CGSOLVER_HPP */
