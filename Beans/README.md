This module calculates the shear force and bending moment of a statically determinate beam which is subjected to several types of loads and moments. Beam can be a simply supported or over hanging.

And creates shear force and bending moment diagram.


Parameters --
    
    length: Length of the beam. (int or float)
    
    support: The support positions of the beam.
         list or tuple of two elements (float, float)
         default: two endpoints of the beam i.e. (0, length)
         
    forces:  External forces and moments applied to the beam
          A list or tuple where every element is also a list or tuple
          
    steps:  Total No. of intervals per unit length
          int, default: 100

    zoom: increases the size figuer (in %)
          float, default: 100
            
    colors: these colors will be assigned to the figures according to order.
          list or tuple of three elements
          default:['#00FF00','#00FFFF','#FF00FF']
            
   
   
Types of forces moments that can be added: 

    Forces:
        1. Concentrrated or Point Load (PL): list or tuple of two elements (float, float).
          first one is the magnitude of the load, second is the position on the beam where this load is acting
        2. Uniformly Distributed Load (UDL), list or tuple of three elements (float, float, float).
          first element represents the magnitude of the distribution of load (force per unit length),
          last two elements represent the span of UDL. (starting & ending position)
        3. Uniformly Varying Load (UVL), list or tuple of four elements (float, float, float, float).
          first two elements represent the magnitude of the distribution of load (force per unit length),
          which is varying linearly (slope can be either positive or negative) along its span.
          last two elements represent the span of UVL. (starting & ending position)
        
    Moments:
        1. Concentrrated or Point Moment (PM), list or tuple of three elements (str, float, float).
        2. Uniformly Distributed Moment (UDM), list or tuple of four elements (str, float, float, float).
        3. Uniformly Varying Moment (UVM), list or tuple of five elements (str, float, float, float, float).
          rules for adding a moment is exactly same as loads except an addidtional string element of 
        value 'm' is required at the first position, to distinguish between a load & monent.
        
        
Example:
    
    sfd_bmd_ssb(length=20, support=(1,19), forces=[(10, 10), ('m', 3, 8, 5, 15)], steps=200)
