#include <boost/multi_array.hpp>
#include <iostream>
#include <stdlib.h>
#include <string>

#include "hw6.hpp"
#include "image.hpp"

/*instantiating constructor for image class. Constructor takes in a string 
name input, and stores the input file name. ReadGrayscaleJPEG then reads 
in the image data and stores the pixels values in the boost 
array named img. The output and sharpness calculation boost arrays
are also instantiated in the constructor*/
image::image(std::string input) {
    this -> input = input;
    this -> img = img;

    // reading in image data
    ReadGrayscaleJPEG(input, img);
    
    this -> output.resize(boost::extents
        [(int)img.shape()[0]][(int)img.shape()[1]]);
    
    this -> sharpness.resize(boost::extents
        [(int)img.shape()[0]][(int)img.shape()[1]]);

    this -> output = img;
}

/* function overloading for the save function. If the user provides 
an output name, save the image to the output name. If not, save 
the image under the same name as the input.*/
void image::Save() {
    WriteGrayscaleJPEG(this->input, this->output);
}

void image::Save(std::string outputstr) {
    WriteGrayscaleJPEG(outputstr, this->output);
}

/*The convolution function calculates the value of each pixel in the 
output image. In order to handle edge cases, a larger temp array is 
created. The temp array extends the input array on all four sides in
order to accomodate convolution calculations for the pixels on 
the edge of the input image. Each output pixel is calculated by 
summing the product of each kernel value and the cooresponding
input image pixel value. The function takes in an input boost array with 
the input image pixels, an instantiated but empty output boost array,
and a kernel value boost array.*/
void image::Convolution(const boost::multi_array<unsigned char,2>& input,
    boost::multi_array<unsigned char,2>& output,
    const boost::multi_array<float,2>& kernel) {
        unsigned int input_rows = (unsigned int)input.shape()[0];
        unsigned int input_cols = (unsigned int)input.shape()[1];
        
        unsigned int output_rows = (unsigned int)output.shape()[0];
        unsigned int output_cols = (unsigned int)output.shape()[1];

        unsigned int kernel_rows = (unsigned int)kernel.shape()[0];
        unsigned int kernel_cols = (unsigned int)kernel.shape()[1];
        
        /*Error checks that the input, output, and kernel arrays fit the image
        specifications.*/
        if (output_rows != input_rows || output_cols != input_cols) {
            std::cout << "Input and Output dimensions do not match" 
                << std::endl;
            exit(0); // exit the program
        }

        if (kernel_rows != kernel_cols) {
            std::cout << "Kernel is not square" << std::endl;
            exit(0); // exit the program
        }

        if (kernel_rows < 3 || kernel_cols < 3) {
            std::cout << "Kernel is too small" << std::endl;
            exit(0); // exit the program 
        }
  
        if (kernel_rows % 2 == 0 || kernel_cols % 2 == 0) {
            std::cout << "Kernel size is not odd" << std::endl;
            exit(0); // exit the program 
        }
        
        unsigned int temp_rows = input_rows + (2 * (kernel_rows - 1)/2);
        unsigned int temp_cols = input_cols + (2 * (kernel_cols - 1)/2);

        /*Instantiates a larger temp boost array to store the expanded 
        input boost array. This takes care of the edge cases in 
        calculating kernel values.*/
        boost::multi_array<unsigned char,2> temp
            (boost::extents[temp_rows][temp_cols]);

        unsigned int added_vals = (kernel_rows - 1)/2;
       /*call helper function to create large matrix*/
        image::create_temp_array(input, temp, input_rows, input_cols, 
            added_vals);
        /*compute the convolution*/
        for (unsigned int row = 0; row < input_rows; row ++) {
            for (unsigned int col = 0; col < input_cols; col++){
                float output_val = 0;
                for (unsigned int temp_row = 0; temp_row < kernel_rows;
                    temp_row ++) {
                    for (unsigned int temp_col = 0; temp_col < kernel_cols;
                        temp_col ++){
                        output_val += 
                            ((float)temp[temp_row + row][temp_col + col] * 
                            kernel[temp_row][temp_col]); 
                    }
                }

            /*correcting for overflow/underflow errors*/
            if (output_val < 0) {
                output_val = 0;
            }
            else if (output_val > 255) {
                output_val = 255;
            }
            output[row][col] = (unsigned char)floor(output_val);
            
        }
    }
}

void image::create_temp_array(const boost::multi_array<unsigned char,2>& input,
    boost::multi_array<unsigned char,2>& temp, unsigned int &input_rows,
    unsigned int &input_cols, unsigned int &added_vals) {
    /* fill the extended temp array with known values from the input*/
    for (unsigned int row = 0; row < input_rows; row ++) {
        for (unsigned int col = 0; col < input_cols; col ++) {
            temp[row + added_vals][col + added_vals] = input[row][col];
        }
    }
    /* fill in the four corners of the temp array*/
    for (unsigned int row = 0; row < added_vals; row ++) {
         for (unsigned int col = 0; col < added_vals; col ++) {
            if ((row != added_vals) & (col != added_vals)) {
                temp[row][col] = input[0][0];
                temp[row + input_rows + added_vals][col] =
                    input[input_rows - 1][0];
                temp[row][col + input_cols + added_vals] =
                    input[0][input_cols - 1];
                temp[row + input_rows +
                    added_vals][col + input_cols + added_vals] =
                    input[input_rows - 1][input_cols - 1];
             }
         }
    }
     /* fill in the outer columns of the temp array*/
    for (unsigned int row = 0; row < added_vals; row ++) {
        for (unsigned int col = 0; col < input_cols; col ++) {
            temp[row][col + added_vals] = input[0][col];
            temp[row + input_rows + added_vals][col + added_vals]
                = input[input_rows - 1][col];
        }
    }
    /* fill in the outer rows of the temp array*/
    for (unsigned int col = 0; col < added_vals; col ++) {
        for (unsigned int row = 0; row < input_rows; row ++) {
            temp[row + added_vals][col] = input[row][0];
            temp[row + added_vals][col + input_cols +added_vals]
                = input[row][input_cols - 1];
        }
    }
}

/*The BoxBlur function creates the scaled to 1 all ones kernel
and applies it to the input image using the convolution function
The blurred output image is stored in the instantiated output array.*/
void image::BoxBlur(unsigned int size) {
    boost::multi_array<float,2> kernel(boost::extents[size][size]);
    float n = (float)size * (float)size;
    for (unsigned int i = 0; i < size; i++) {
        for (unsigned int j = 0; j < size; j++) {
            kernel[i][j] =1/n;
        }
    }
    image::Convolution(this -> img, this ->output, kernel);
}


/*The Sharpness function creates the laplacian kernel and 
applies it to the output image using the convolution function.
The maximum value of the resulting output can be used to 
quantify the sharpness of the image.*/
unsigned int image::Sharpness() {
    boost::multi_array<float,2> kernel(boost::extents[3][3]);
    kernel[0][0] = 0;
    kernel[0][1] = 1;
    kernel[0][2] = 0;
    kernel[1][0] = 1;
    kernel[1][1] = -4;
    kernel[1][2] = 1;
    kernel[2][0] = 0;
    kernel[2][1] = 1;
    kernel[2][2] = 0;
    
    image::Convolution(this ->output, this ->sharpness, kernel);
    unsigned int max_val = 0;
    for (unsigned int row = 0; row < sharpness.shape()[0]; row ++) {
        for (unsigned int col = 0; col < sharpness.shape()[1]; col++) {
            if ((unsigned int)sharpness[row][col] > max_val) {
                max_val = (unsigned int)sharpness[row][col];
            }
        }
    }
    return max_val;
}
         
