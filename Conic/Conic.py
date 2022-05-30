import matplotlib.pyplot as plt
import numpy as np

class Point:
    def __init__ (self, x, y):
        self.value = (x,y)
        self._x = x
        self._y = y
        
    def __str__ (self):
        return (f'({self._x},{self._y})')
    
    def __add__ (self, other, /):
        sum_x = self._x + other._x
        sum_y = self._y + other._y
        return Point(sum_x, sum_y)

class _Conic :
    _x_initial, _y_initial = 0, 0
    def __init__ (self, h=0, k=0):
        """Define a Conic section.
        h = x co-ordinate of the center
        k = y co-ordinate of the center
        """
        self._x_center, self._y_center = h, k
        self.center = (self._x_center, self._y_center)
        
    def translate(self, shift=(0,0)):                 # Shifts the midpoint of conic.
        self._x_center = self._x_center + shift[0]    
        self._y_center = self._y_center + shift[1]
        self.center = (self._x_center, self._y_center)
     
    def rotate(self, angle=0):                    # Rotation remaining center point fixed.
        if angle!=0:                              # reset to zero, if previously rotated.
            self._x = self._x_initial
            self._y = self._y_initial
        self.angle = angle                        # In degrees.
        theta = np.deg2rad(self.angle)            # Converting into radians.
        rotation_matrix = np.array([[np.cos(theta), -np.sin(theta)],
                                    [np.sin(theta),  np.cos(theta)]])
        R_11, R_12 = rotation_matrix[0][0], rotation_matrix[0][1]
        R_21, R_22 = rotation_matrix[1][0], rotation_matrix[1][1]
        self._x = self._x_initial*R_11 + self._y_initial*R_12   # x-coordinates of locus after rotating.
        self._y = self._x_initial*R_21 + self._y_initial*R_22   # y-coordinates of locus after rotating.
        
    def draw(self, c='b', zoom=100, midpoint=True):
        """Drawing the conic section"""
        fig_size = list(map(lambda x:x*zoom/100, plt.rcParams.get('figure.figsize')))
        try:                      # If it is transformed.
            x_points = self._x + self._x_center
            y_points = self._y + self._y_center
        except AttributeError:    # If it is NOT transformed.
            x_points = self._x_initial + self._x_center
            y_points = self._y_initial + self._y_center
        
        fig1 = plt.figure(1, figsize=fig_size)
        plt.plot(x_points,y_points,c)
        if midpoint==True:         # To plot the Middle point.
            plt.plot(self._x_center, self._y_center, marker='o', markersize=5)
        plt.grid() 
        plt.axis("scaled")

class Ellipse(_Conic):
    def __init__ (self, a, b=None, h=0, k=0, edges=300):
        """Creates an ellipse
        a = Horizontal radius
        b = Vertical radius, if not provided, b will be equal to a.
        h = x co-ordinate of the center
        k = y co-ordinate of the center
        """
        super().__init__ (h, k)
        if b==None:
            b = a
        self._horiz_rad, self._vert_rad = a, b
        self.cemimajor_axis = max(a,b)
        self.cemiminor_axis = min(a,b)
        self.edges = edges
        t = 2*np.pi*(np.linspace(0,1,self.edges))
        self._x_initial = self._horiz_rad*(np.cos(t))
        self._y_initial = self._vert_rad*(np.sin(t))
        
    @property    
    def auxilliary_circle(self):
        center = (self._x_center, self._y_center)
        rad = self.cemimajor_axis
        return Circle(r=rad, h=center[0], k=center[1])

class Circle(_Conic):
    def __init__ (self, r, h=0, k=0, edges=300):
        """Creates an circle
        r = radius of the circle
        h = x co-ordinate of the center
        k = y co-ordinate of the center
        """
        super().__init__ (h, k)
        self.radius = r
        self.edges = edges
        t = 2*np.pi*(np.linspace(0,1,self.edges))
        self._x_initial = self.radius*(np.cos(t))
        self._y_initial = self.radius*(np.sin(t))
        
class Hyperbola(_Conic):
    def __init__ (self, a, b=None, h=0, k=0, edges=300):
        super().__init__ (h, k)
        self.cemimajor_axis = a
        self.cemiminor_axis = b
        if b==None:
            b = a
        self.edges = edges
        t = 2*np.pi*(np.linspace(0,1,self.edges))
        self._x_initial = self.cemimajor_axis*(1/np.cos(t))
        self._y_initial = self.cemiminor_axis*(np.tan(t))
        
    def draw(self, c='b', zoom=100):
        super().draw(c, zoom, midpoint=False)
        plt.xlim((self._x_center-10*self.cemimajor_axis), (self._x_center+10*self.cemimajor_axis))
        plt.ylim((self._y_center-10*self.cemiminor_axis), (self._y_center+10*self.cemiminor_axis))
        
class Parabola(_Conic):
    def __init__ (self, p, h=0, k=0, edges=300):
        super().__init__ (h, k)
        self.vertex = (h, k)
        self.rate = p
        self.edges = edges
        t_rev = np.linspace(10,0,self.edges)
        x_upper = p*np.square(t_rev)
        y_upper = 2*p*t_rev
        x_lower = (p*np.square(t_rev[::-1]))
        y_lower = -2*p*t_rev[::-1]
        self._x_initial = np.concatenate([x_upper,x_lower])
        self._y_initial = np.concatenate([y_upper,y_lower])
