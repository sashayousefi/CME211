In this project, we were given the task to find a solution to a maze using 
the right hand rule. In the right hand rule, the maze goer simply 
starts with their right hand on the wall and follows the wall 
until they find the exit. The maze goer is switching orientations 
as they follow the maze, and so when writing the algorithm, one must 
account for orientation switches between north, south, east, and west 
in order to consistently follow the right hand rule. Once we find a solution,
we store it in a text file, and check its validity using a separate program. 

In the C++ code, I first define the maximum columns and rows the maze can 
take on in order to specifiy dimensions for static maze array. The benefits
of utilizing a static array are that they are allocated memory at compile time,
which is more efficient. Since we know the size of the largest maze, we can 
set the 2d static array to contain the largest possible dimensions (201 x 201).
I initialize the maze array to all zeros prior to running the program.
After checking that the correct amount of input arguments are given, I read 
the maze file into the the program, checking that the static array has enough
storage before preceeding. If it does, I begin adding wall positions in the 
static array. If a wall exists at a particular row/column coordinate, I add 
a one in place of the initialized zero. Once this portion of the program 
runs, I have a 2d array indicating the locations of the walls in the maze.

Next, I find the entrance column for the maze, doing so by finding the empty
column position at row 0, and write it to the solution file. I then run 
the algorithm to solve the maze using the right hand rule. Since there are 
four orientations for the maze goer (North, South, East, and West), I look 
at these at a case by case basis to make decisions on where to move next 
while accounting for the orientation that the maze goer is currently in. 
In the right hand rule, the maze goer always tries to proceed right first. 
If the right movement is unavailable, the maze goer proceeds straight until 
a right slot is available, or they reach a wall in front of them. If a wall
is reached and there is no right slot available, the maze goer proceeds left 
of the orientation that they are currently in. It is important to note 
that notions of right, left, reverse, and straight change with the player's
orientation. For example, if the player is facing south, the "right" direction 
is considered west of where the player currently is. However, if the player 
was facing north, "right" would be to the east. So if we are considering the 
latter case and the player was able to move right, then the direction for the 
maze goer would change from north to east. The only time we do not change 
direction orientation is when the player is moving straight. In that case, 
"south" remains "south" and so on. 

As I run through these position changes, I store the next position in an 
output text file, and proceed with the loop until the maze has been solved. 
I make sure to return 0 at each break point of the program and the program 
end so that the program compiles properly. 

In addition to the maze solution file, I also created a checksoln.py file, 
which checks the validity of the maze solution. First, the file checks 
for appropriate inputs (a maze and a solution file) and exits if they were 
not given. After loading in the maze and solution file, I create a dictionary 
of maze walls. In this dictionary, I store the row coordinates as keys and the 
column coordinates as values. Using this dictionary, we can check the existance
of a wall at a particular coordinate. 

The main function of this checksoln file is the check_solution function. In 
this function, I check a number of criteria to ensure that a solution is valid.
I check that the player entered the maze on the first row. I do this by 
checking that the user entered the maze on row 0 and the correct entrance
column position. Next, I check that each position change is valid (i.e. 
the player moves one position at a time, doesn't go through a wall, and stays
within the bounds of the maze). To check that the player moves one position
at a time, I check that the player does not net more than +/-1 change in
position sum from the previous coordinate. To check that the player doesn't 
go throguh a wall, I check that no coordinates in the solution file 
overlap with coordinates in the wall dictionary. To check that the player
stays in the bounds of the maze, I check that no coordinates in the solution
file exceed the row and column dimensions of the maze. If all these checks 
pass, the solution is valid! If not, something went wrong. 

Thanks for reading!


