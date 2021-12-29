import glob
import math
import os

"""
Airfoil class: collection of different methods calculating 
the parameters of the airfoil, 2D cross section of a wing,
at multiple angles of attack.

This module defines methods for calculating the lift coefficient 
and stagnation points for a particular angle of attack on an airfoil.
These utilities would be of interest to someone who may be interested
in wing design
"""
class Airfoil:
    def __init__(self, inputdir):
        """
        Initializes all public and private variables in
        the program. Takes as an input the input directory. Stores
        the edges, chord length, alpha values, lift coefficient, and
        stagnation list while the program is running through the
        methods for different alpha angles of attacks.
        """
        self.inputdir = inputdir
        self.__edges = {}
        self.__chordlen = 0
        self.__alpha_vals = {}
        self.__lift_coeff = {}
        self.__stagnation_lst = {}
        self.run_functions()

    def get_xy(self):
        """
        retrieves the (x,y) attributes for a series of points along the
        airfoil.This method checks existence of the coordinate data file,
        checks that the values are parsable numerically and
        in an (x,y) format. Collects (x,y) positions and stores them 
        in a dictionary indicating their respective position along the 
        airfoil. 
        """ 
        self.xy_file = os.path.join(self.inputdir, "xy.dat")
        if not os.path.isfile(self.xy_file):
            raise RuntimeError('xy.dat file is not found in given directory')
        with open(self.xy_file, 'r') as xy:
            self.airfoil = xy.readline().strip()
            self.coord_position = 1
            while True:
                coords = xy.readline().strip().split()
                if coords == []:
                    break;
                if len(coords) != 2:
                    raise RuntimeError('datafile must have an x and y value')
                try:
                    x = float(coords[0])
                    y = float(coords[1])
                except:
                    raise RuntimeError('x and y cannot be case numerically')
                self.__edges[self.coord_position] = [x, y]
                self.coord_position += 1
                 
    def compute_chordlen(self):
        """
        Computes the chordlength for the airfoil by taking the span 
        of the airfoil geometry along the x axis (ie. the distance
        from the trailing edge to the leading edge of the airfoil
        in 2d space). 
        """
        x_lst = [x[0] for x in self.__edges.values()]
        trailing = list(self.__edges.values())[x_lst.index(max(x_lst))]
        leading = list(self.__edges.values())[x_lst.index(min(x_lst))]
        self.__chordlen = math.sqrt((trailing[0] - \
            leading[0])**2 + (trailing[1] - leading[1])**2)
        return self.__chordlen
                
    
    def get_alphas(self):
        """
        Retrieve pressure reading values for each panel of the airfoil while
        under each alpha (angle) level of attack. The method checks 
        that alpha files exist for the particular airfoil, that 
        the alpha values are numerical, and that pressure readings are 
        able to be parsed numerically. The method collects all the 
        pressure reading values per alpha and stores them in a 
        nested dictionary. The first layer contains the alpha
        value as the key and the pressure value dictionary for that 
        alpha as a value. The second layer contains the panel_id 
        as the key and the pressure coeff as the value.
        """
        alphas = glob.glob(os.path.join(self.inputdir, "alpha*.?.dat"))
        if len(alphas) == 0:
            raise RuntimeError("no alpha values found")
        for alpha in alphas:
            try:
                angle = float(alpha.split('alpha')[1].split('.dat')[0])
            except:
                raise RuntimeError('alpha value is non numerical')
            with open(alpha, 'r') as alph:
                panel_idx = 1
                title = alph.readline().strip()
                pressure_coeff = {}
                for line in alph:
                   try:
                      cp = float(line.strip())
                   except:
                       raise RuntimeError("unable to parse pressure readings")
                   pressure_coeff[panel_idx] = cp
                   panel_idx += 1
            self.__alpha_vals[angle] = pressure_coeff
    
    def compute_deltas(self, alpha):
        """
        computes and stores the delta_cx, and delta_cy values - the components 
        in the x and y direction of the non dimensional force acting
        perpendicular to the panel. Additionally, the method computes 
        and stores the stagnation point for the specified alpha. 
        The stagnation point is where the flow velocity goes to 0
        or equivalently when the pressure coefficient goes to 1.0.
        The delta_cx and delta_cy are returned as lists. The stagnation
        point is stored as a list containing the pressure coefficient 
        at the point along with mean of the x and y panel values. 
        """
        stagnation = [0, 0, 0]
        deltas = {}
        delta_cx, delta_cy = [],[]
        for i in range(1, len(self.__edges)):
            delta_x = self.__edges[i+1][0] - self.__edges[i][0]
            delta_y = self.__edges[i+1][1] - self.__edges[i][1]
            deltas[i] = [delta_x, delta_y]
        for panel_id in range(1, len(self.__edges)):
            cp = self.__alpha_vals.get(alpha).get(panel_id)
            if cp > stagnation[2]:
                avgx=(self.__edges[panel_id+1][0]+self.__edges[panel_id][0])/2
                avgy=(self.__edges[panel_id+1][1]+self.__edges[panel_id][1])/2
                stagnation = [avgx, avgy, cp]
            dx = deltas.get(panel_id)[0]
            dy = deltas.get(panel_id)[1]
            delta_cx.append((-1) * cp * dy / self.__chordlen)
            delta_cy.append(cp * dx / self.__chordlen)
            self.__stagnation_lst[alpha] = stagnation
        return delta_cx, delta_cy

    def compute_lift_coefficient(self, alpha):
        """
        Computes the lift coefficients for each alpha : the difference 
        between 1 and 2:
        1. the sum of the delta_cy (the y component of the 
        non dimensional perpendicular force on the plane) * cos(alpha)
        2. the sum of the delta_cx (the x component of the 
        non dimensional perpendicular force on the plabe) * sin(alpha)

        stores this value in a dictionary with alpha (angle of attack)
        as the key and the lift coefficient as the value.
        """
        delta_cx, delta_cy = self.compute_deltas(alpha)
        lift_coeff = sum(delta_cy) *math.cos(math.radians(alpha)) - \
            sum(delta_cx)*math.sin(math.radians(alpha))

        self.__lift_coeff[alpha] = lift_coeff 
        return self.__lift_coeff
        

    def run_functions(self):
        """
        Main method that runs all the functions above and computes all the 
        values necessary to calculate the lift coefficient and stagnation 
        point for each alpha. This function checks the following inputs:
        1. that the directory exists
        2. that the input only invokes one path
        3. That the directory is a valid directory
        """
        direcs = glob.glob(os.path.join(os.getcwd(), self.inputdir), \
            recursive = True)
        if len(direcs) == 0:
           raise RuntimeError('{} : does not exist'.format(self.inputdir))
        elif len(direcs) > 1:
            raise RuntimeError('{}: invokes multiple paths'.\
                format(self.inputdir))
        else:
            self.inputdir = direcs[0]
            if not os.path.isdir(self.inputdir):
                raise RuntimeError ('{} : not a valid directory'\
                    .format(self.inputdir))
        self.get_xy()
        self.compute_chordlen()
        self.get_alphas()
        for alpha in self.__alpha_vals:
            self.compute_lift_coefficient(alpha)

    def __repr__(self):
        """
        Method that returns the string to be printed as invoked by 
        main.py. Properly formats the alpha values, lift coefficient,
        and stagnation point in our data. The output we expect 
        from the __repr__ are the lift coefficient and stagnation point
        for each alpha value in a tabular format.
        """
        main_str = ''
        main_str += 'alpha     cl           stagnation pt\n'
        main_str += '-----  -------  --------------------------\n'
        for alpha in sorted(self.__alpha_vals):
            cl = round(self.__lift_coeff[alpha],8)+0
            stag_lst = self.__stagnation_lst[alpha]
            stag_pt_x, stag_pt_y, stag_cl = round(stag_lst[0],8)+0 \
                , round(stag_lst[1],8)+0, round(stag_lst[2],8)+0
            main_str+=('{: 5.2f}  {: 5.4f}  ({: 5.4f}, {: 5.4f}) {: 5.4f}\n')\
                .format(alpha, cl, stag_pt_x, stag_pt_y, stag_cl)
        return main_str
        
