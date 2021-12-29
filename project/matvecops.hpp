#ifndef matvecops_HPP
#define matvecops_HPP

#include <vector>

/* HPP file containing common matrix operations */
std::vector<double> mat_vec_prod(const std::vector<int> &rowptr,
                                 const std::vector<int> &colidx,
                                 const std::vector<double> &val,
                                 const std::vector<double> &vec);

double L2_norm(const std::vector<double> &vec);

double dot_prod(const std::vector<double> &vec1,
                const std::vector<double> &vec2);

std::vector<double> scalar_vec_prod(const std::vector<double> &vec,
                                    const double &scalar);


std::vector<double> vec_add_sub(const std::vector<double> &vec1,
                                    const std::vector<double> &vec2,
                                    const int &op);

#endif /* matvecops_HPP */
