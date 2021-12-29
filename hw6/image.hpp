#ifndef IMAGE_HPP
#define IMAGE_HPP
#include <string>
#include <boost/multi_array.hpp>

class image {
    std::string input;
    boost::multi_array<unsigned char, 2> img;
    boost::multi_array<unsigned char, 2> output;
    boost::multi_array<unsigned char, 2> sharpness;
    public:
        image(std::string input);
        void Save();
        void Save(std::string outputstr);
        void Convolution(const boost::multi_array<unsigned char,2>& input,
            boost::multi_array<unsigned char,2>& output,
            const boost::multi_array<float,2>& kernel);
        void create_temp_array(const boost::multi_array<unsigned char,2>& input,
        boost::multi_array<unsigned char,2>& temp, unsigned int &input_rows,
        unsigned int &input_cols, unsigned int &added_vals);
        void BoxBlur(unsigned int size);
        unsigned int Sharpness();
};

#endif /* IMAGE_HPP */
