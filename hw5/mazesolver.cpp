#include <iostream>
#include <fstream>
#include <string>
using std::cout;
using std::string;

int main(int argc, char *argv[]) {
/* Main function which reads in maze dimensions, finds the solution to the maze
using the right hand wall follower algorithm, and creates an output file with 
the solution of the maze written into the file*/

    #define max_rows 201
    #define max_cols 201
    int arr[max_rows][max_cols]= {0};
    int entrance_col = 0;
    int len_rows, len_cols;

    //checks for the correct number of inputs in the command line
    if (argc != 3){ 
        cout << "Usage:\n";
        cout << "./mazesolver <maze file> <solution file>\n";
        return 0; //quits the program if incorrect number of args
    }
    std::string filename = argv[1];
    std::string output = argv[2];
    
    //reads the maze into a two dimensional array 
    std::ifstream f(filename); 
    if (f.is_open()) {
        f >> len_rows >> len_cols;
        if (len_rows > max_rows or len_cols > max_cols) {
            std::cout << 
                "Not enough space in the static array to store the maze" 
                 << std::endl;
            return 0; // quit the program if there is not enough storage
        }
        int row; int col;
        while (f >> row >> col) {
            arr[row][col] = 1;
        }
        f.close();
       
        //finds the entrance column for the maze
        for (int i = 0; i < len_cols; i++){
            if (arr[0][i] == 0){
               entrance_col = i;
            }
        }
        f.close();  
    }
    //opens the output file and begins writting the solution into the file
    std::ofstream g(output);
    if (g.is_open()) {
        //write the entrance position into the solution file 
        g << std::to_string(0) << " " << std::to_string(entrance_col) 
            << std::endl;
        g << std::to_string(1) << " " << std::to_string(entrance_col)
            << std::endl;
        
        enum direction {North, South, East, West};
	direction d = South;
        int r_counter = 1;
        int c_counter = entrance_col;
        /*Uses a switch function to change position orientation while traveling
        through the maze. Uses the right hand rule to travel through the maze, 
        check moving right first, straight next, left third, and reverse last. 
        Exact movements depend on orientation, so four case conditions are 
        written to determine exact movement based on orientation.*/
        while (r_counter < (len_rows - 1)) {         
            switch (d) {
                case South:
                   if (arr[r_counter][c_counter - 1] == 0){
                       c_counter -= 1;
                       d = West;
                       } 
                   else if (arr[r_counter+1][c_counter] == 0) {
                       r_counter += 1;
                       break;
                       }
                   else if (arr[r_counter][c_counter +1] == 0) {
                       c_counter += 1;
                       d = East;
                       }
                   else {
                       r_counter -= 1;
                       d = North; 
                       }
                   break;
               case North:
                   if (arr[r_counter][c_counter+1] == 0){
                       c_counter += 1;
                       d = East; 
                       }
                   else if (arr[r_counter-1][c_counter] == 0) {
                       r_counter -= 1;
                       }
                   else if (arr[r_counter][c_counter-1] == 0){
                       c_counter -= 1;
                       d = West;
                       }
                   else {
                       r_counter += 1;
                       d = South; 
                       }
                   break;
               case East:
                   if (arr[r_counter+1][c_counter] == 0){
                       r_counter += 1;
                       d = South; 
                       }
                   else if (arr[r_counter][c_counter + 1] == 0) {
                       c_counter += 1;
                       }
                   else if (arr[r_counter - 1][c_counter] == 0){
                       r_counter -= 1;
                       d = North;
                       }
                   else {
                       c_counter -= 1;
                       d = West;
                       }
                   break;
                case West:
                   if (arr[r_counter-1][c_counter] == 0){
                       r_counter -= 1;
                       d = North;
                       }
                   else if (arr[r_counter][c_counter-1] == 0) {
                       c_counter -= 1;
                       }
                   else if (arr[r_counter+1][c_counter] == 0){
                       r_counter += 1;
                       d = South;
                       }
                   else {
                       c_counter += 1;
                       d = East;
                       }
                   break;
                }
            /*writes the current position into the maze before searching for
            the next position*/ 
            g << std::to_string(r_counter) << " " 
                << std::to_string(c_counter) << std::endl;
        }
    g.close();
   
   }
 return 0;
}
    



    
