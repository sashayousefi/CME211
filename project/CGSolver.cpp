#include <cmath>
#include <fstream>
#include <iostream>
#include <iomanip>
#include <sstream>
#include <string> 

#include "CGSolver.hpp"
#include "matvecops.hpp"
#include "sparse.hpp"

/* Implement the CG solver algorithm according to the psuedocode 
given in the assignment. In this iteration of CGsolver, 
we implement the algorithm using a sparse matrix 
object, which we pass in by reference. We add functions in 
our sparse matrix class which are able to compute and 
store the CSR implementations of the matrix as well 
as compute matrix vector products. These functionalities 
are utilized in our CGSolver to implement our algorithm 
using object oriented programming.*/ 

int CGSolver(SparseMatrix &A,
             const std::vector<double> &b,
             std::vector<double> &x,
             double              tol,
             std::string soln_prefix,
             unsigned int nrows, unsigned int ncols) { 

    std::vector<double> Au = A.MulVec(x);
    std::vector<double> r = vec_add_sub(b, Au, -1);
    double L2normr0 = L2_norm(r);
    std::vector<double> p = r;
    int niter = 0;
    //write the starting solution to a solution file.
    write_soln(soln_prefix, x, niter, ncols, nrows, b);
    int nitermax = (int)std::pow(A.get_size() - 1, 2);
    while (niter < nitermax) {
        //write our solution to a solution file every 10 iterations
        if (niter % 10 == 0) {
            write_soln(soln_prefix, x, niter, ncols, nrows, b);
        }
        niter += 1;
        std::vector<double> Apn = A.MulVec(p);
        double alpha = dot_prod(r, r)/dot_prod(p, Apn);
        std::vector<double> scaled_vec = scalar_vec_prod(p, alpha);
        x = vec_add_sub(x, scaled_vec, 1);
        std::vector<double> scaled_vec2 = scalar_vec_prod(Apn, alpha);
        std::vector<double> r_next = vec_add_sub(r, scaled_vec2, -1);
        double L2normr = L2_norm(r_next);

        /*exiting the function if our solution has converged to the true 
        solution up to some tolerance threshold*/
        if (L2normr/L2normr0 < tol) {
            break;
        }
        double beta = dot_prod(r_next, r_next)/dot_prod(r, r);
        std::vector<double> scaled_vec3 = scalar_vec_prod(p, beta);
        std::vector<double> p_next = vec_add_sub(r_next, scaled_vec3, 1);
        p = p_next;
        r = r_next;
    }
    //writing final solution to the solution file
    write_soln(soln_prefix, x, niter, ncols, nrows, b);
    if (niter < nitermax){
        return niter;
    }
    else{
        return -1;
    }
}

/*The following function writes the current version of the solution into
a solution file in matrix format. It does so by reporting each currently
approximated (or converged) temperature value of the discritized wall 
as it is located in the pipe wall configuration. This leads to a matrix 
of values which correspond to their positioning in the pipe wall. The solution
includes the isothermal boundaries and both periodic boundaries for a more 
accurate plotting of the isoline later on.*/

void write_soln(std::string soln_prefix, const std::vector<double> &x, int niter,
    unsigned int ncols, unsigned int nrows, const std::vector<double> &b){
    std::stringstream soln_num;
    soln_num << std::setw(3) << std::setfill('0') << std::to_string(niter);
    std::string output_name = soln_prefix + soln_num.str() + ".txt"; 
    std::ofstream g(output_name);
    if (g.is_open()) {
        //add isothermal hot boundary 
        for (unsigned int i = 0; i < b.size(); i += nrows) {
            g << b.at(i) << " ";
        }
        g << b.at(0) << " ";
        g << "\n";
        //add interior nodes
        for (unsigned int i = 0; i < nrows; i++){
            for (unsigned int j = 0; j < ncols; j++){
                g << x.at(i + j*nrows) << " ";
            }
        g << x.at(i) << " ";
        g << "\n";
        }
        //add isothermal cold boundary 
        for (unsigned int i = nrows - 1; i < b.size(); i += nrows) {
            g << b.at(i) << " ";
        }
        g << b.at(nrows - 1) << " ";
        g << "\n";
        g.close();
    }
    else{
        std::cout << "Solution file format is invalid" << std::endl;
        exit(0);
    }
}

