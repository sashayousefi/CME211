#include <iomanip>
#include <iostream>
#include <string>

#include "hw6.hpp"
#include "image.hpp"

int main(){  
   
    /*Define the image to be blurred and call the class constructor */
    std::string input = "stanford.jpg";
    image img(input);
    /*Calculating sharpness for the original image*/
    unsigned int OG_sharpness = img.Sharpness();
    std::cout << "Original image: " << OG_sharpness << " ";

    /*Blurring the image, calculating sharpness, and saving the image*/
    for (unsigned int i = 3; i < 28; i += 4){
        image img(input); //instantiate a new image
        img.BoxBlur(i); //blur the image 
        unsigned int sharp = img.Sharpness(); //calculate sharpness
        std::cout  << "BoxBlur(" << std::setw(2) 
            << i << "): " << sharp << " ";
        std::string output = "";
        
        if (i < 10) {
            output = "BoxBlur" + std::to_string(0) + std::to_string(i);
        }
        else {
            output = "BoxBlur" + std::to_string(i);
        }
        
        img.Save(output + ".jpg"); //saving the image
    }
   std::cout << std::endl; 
}
