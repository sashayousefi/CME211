#include <iostream>
#include <vector>

#include "COO2CSR.hpp"
#include "sparse.hpp"

/*Sparse class which defines the necessary functions and variables
for our Sparse Matrix object These methods are used in our CGSolver
in our heat and CGSolver classes in order to implement object 
oriented programming for our Sparse Matrix.*/

void SparseMatrix::Resize(int nrows, int ncols){
    /*resizes the matrix to get the proper number of rows and columns for
    our */
    this-> ncols = ncols;
    this -> nrows = nrows;
}

void SparseMatrix::AddEntry(int i, int j, double val){
    /*adds entries in our matrix A in COO format, which is the matrix we 
    will use to solve our linear system of unknowns.*/
    this -> i_idx.push_back(i);
    this -> j_idx.push_back(j);
    this -> a.push_back(val);
}
void SparseMatrix::ConvertToCSR(){
    /*uses the provided COO to CSR converter to convert our matrix 
    A to CSR format*/
    COO2CSR(this -> a, this -> i_idx, this -> j_idx);
}

std::vector<double> SparseMatrix::MulVec(std::vector<double> &vec){
    /*Defining matrix vector multiplication for our A matrix object.
    Takes as input a vector "vec" by reference, and matrix vector
    multiplies our A matrix (which is in CSR format) with the 
    provided vector.*/
    int matrix_size = (int)i_idx.size() - 1;
    std::vector<double> result_vector(matrix_size);
    for (int i = 0; i < matrix_size; i ++) {
        result_vector.at(i) = 0;
        for (int j = i_idx.at(i); j < i_idx.at(i+1); j ++) {
           result_vector.at(i) += a.at(j) * vec.at(j_idx.at(j));
        }
    }
    return result_vector;
}

int SparseMatrix::get_size(){
    /*gets the size of the matrix*/
    return (int)i_idx.size();
}
