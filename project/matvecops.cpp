#include <cmath>
#include <iostream>
#include <numeric>
#include <vector>

#include "matvecops.hpp"

/* develop functions in order to compute common matrix/vector operations*/

/* matrix vector product*/
std::vector<double> mat_vec_prod(const std::vector<int> &rowptr,
                                 const std::vector<int> &colidx,
                                 const std::vector<double> &val,
                                 const std::vector<double> &vec) {
    int matrix_size = (int)rowptr.size() - 1;
    std::vector<double> result_vector(matrix_size);
    for (int i = 0; i < matrix_size; i ++) {
        result_vector.at(i) = 0;
        for (int j = rowptr.at(i); j < rowptr.at(i+1); j ++) {
           result_vector.at(i) += val.at(j) * vec.at(colidx.at(j));
        }
    }
    return result_vector;
}


/*L2 norm*/
double L2_norm(const std::vector<double> &vec) {
    double norm = 0;
    for (unsigned i = 0; i < vec.size(); i ++) {
        norm += pow(vec.at(i), 2);
    }
    return sqrt(norm);
}

/*dot product*/
double dot_prod(const std::vector<double> &vec1,
                const std::vector<double> &vec2) {
    double prod = 0;
    for (unsigned i = 0; i < vec1.size(); i++) {
        prod += vec1.at(i) * vec2.at(i);
    }
    return prod;
}

/*scalar vector product*/
std::vector<double> scalar_vec_prod(const std::vector<double> &vec,
                                    const double &scalar) {
    std::vector<double> scaled_vec(vec.size());
    for (unsigned i = 0; i < vec.size(); i++) {
        scaled_vec.at(i) = scalar * vec.at(i);
    }
    return scaled_vec;
}

/*vector addition/subtraction*/
std::vector<double> vec_add_sub(const std::vector<double> &vec1,
                                    const std::vector<double> &vec2, 
                                    const int &op) {
    std::vector<double> result_vec(vec1.size());
    if (op == -1) {
        for (unsigned i = 0; i < vec1.size(); i++) {
            result_vec.at(i) = vec1.at(i) - vec2.at(i);
        }
    }
    else {
        for (unsigned i = 0; i < vec1.size(); i++) {
            result_vec.at(i) = vec1.at(i) + vec2.at(i);
        }
    }
    return result_vec;
}

