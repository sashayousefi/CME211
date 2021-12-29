#include <cmath>
#include <fstream>
#include <iostream>
#include <tgmath.h>
#include <vector>

#include "CGSolver.hpp"
#include "heat.hpp"
#include "sparse.hpp"

/*Created a HeatEquation class which constructs and solves the linear 
system of equations to solve the heat equation. The class consists
of a setup portion and a solve portion. The setup portion organizes 
the system of unknowns into matrix format utilizing a sparse matrix
object. The solve portion of the class passes our designed matrix
into CG Solver, which iteratively solves the system of 
linear equations by converging to the true solution.*/

/*The setup function takes in as objects an input file, from 
which we can read in attributes of the pipe wall, such as dimension and 
temperatures of the isothermal boundaries. With this data, we are able
to set up our system of linear equations by utilizing a (n*m) x (n*m)
symmetric matrix. In our matrix, each point in the discretized wall 
is set up as a linear equation using information from surrounding 
points. The neighboring points will also be unknown (and included 
in the A matrix) if they are not at the boundaries. If the neighboring 
points are at the isothermal boundary, they will be added to the solution
vector.*/

int HeatEquation2D::Setup(std::string inputfile){
    double Tc, Th;
    double length;
    double width;
    double h;
    std::ifstream f(inputfile);
    if (f.is_open()) {
        f >> length >> width >> h;
        f >> Tc >> Th;
        f.close();
    }
    else{
        std::cout << "Input file in improper format: unable to read or open" 
            << std::endl;
        exit(0);
    }
    ncols = (unsigned int)(length/h); 
    nrows = (unsigned int)(width/h) - 1;
    this -> x.resize(ncols*nrows, 1.0);
    this -> b.resize(ncols*nrows, 0.0);
    A.Resize(nrows, ncols);
    //organizing our system of linear equations into matrix format
    for (int j = 0; j < ncols; j ++) {
        for (int i = 0; i < nrows; i ++) {
            int middle = i + j*nrows;
            int above = middle - 1;
            int below = middle + 1;
            int left = (ncols*nrows + (middle - nrows)) % (ncols * nrows);
            int right = (ncols*nrows + (middle + nrows)) % (ncols*nrows);
            //add diagonal entry
            A.AddEntry(middle, middle, 4.0);
            //add left entry
            A.AddEntry(middle,left, -1.0);
            //add right entry
            A.AddEntry(middle,right, -1.0);
            if (i > 0) {
                A.AddEntry(middle, above, -1.0);
            }
            else{
                b.at(middle) += Th; //isothermal hot boundary condition
            }
            if (i < nrows - 1) {
                A.AddEntry(middle, below, -1.0);
             }
            else {
               double T_x = -Tc*(exp(-10*pow((j*h - length/2), 2)) - 2);
               b.at(middle) += T_x; //isothermal cold boundary condition
             }
        }    
    } 
    A.ConvertToCSR(); //modify COO matrix object into a CSR object
    return 0;
}

/*The solve function in the HeatEquation2d class simply 
passes our sparse matrix object, solution vector, 
initial guess vector, and tolerance into our CGSolver function 
in order to calculate the number of iterations (if possible)
to reach convergence. The additional parameters passed into CGSolver
assist in organization of the output files. Returns number of iterations
to reach convergence (if applicable).*/

int HeatEquation2D::Solve(std::string soln_prefix){
    double tol = 1e-5;
    int niter = CGSolver(A, b, x, tol, soln_prefix, nrows, ncols);
    if (niter == -1) {
        std::cout << "FAILURE: CG Solver did not converge in max iterations" 
            << std::endl;
       }
    else{
        std::cout << "SUCCESS: CG solver converged in " << niter << 
            " iterations." << std::endl;
        }
   return 0;
}
