import matplotlib.pyplot as plt

def sfd_bmd_ssb(length, support=(None,None), forces=None, steps=100, zoom=100, colors=['#00FF00','#00FFFF','#FF00FF']):
    """Creates shear force and bending moment diagram for a simply supported beam subjected to several types of loading
    Parameters
    ----------
    length: int or float
            Length of the simply supported beam.
    support: (float, float) default: two endpoints of beam
            The support positions of the beam.
    forces: A list or tuple where every element is also a list or tuple
            External forces and moments applied to the beam
    steps: int, default: 100
            Total No. of intervals per unit length
    zoom: float, default: 100
            increases the size figuer (in %)
    colors: list or tuple of three elements, default:['#00FF00','#00FFFF','#FF00FF']
            these color will be assigned to the figures according to order.
            """
    # Extracting the applied forces, moments and corresponding distances.
    ext_loads, load_distances, ext_moments = [], [], []
    point_moments, all_dist_val = [], []
    for ele in forces:
        if len(ele)==2:  # If the load is the point load.
            if isinstance(ele[0], (int, float)):
                ext_loads.append(ele[0])
                load_distances.append(ele[1])
                ext_moments.append(ele[0]*ele[1])
                all_dist_val.append(ele[1])
            else: raise TypeError ("Unknown type of force or moment")
        elif len(ele)==3:
            if isinstance(ele[0], (int, float)): # If it is Uniformly distributed load.
                equivalent_force = ele[0]*(ele[2] - ele[1])
                cog = sum(ele[1:3])/2
                ext_loads.append(equivalent_force)
                load_distances.append(cog)
                ext_moments.append(equivalent_force*cog)
                all_dist_val.extend([ele[1],ele[2]])
            elif ele[0]=='m':   # If it is concentrated moment.
                point_moments.append(ele[1])
                all_dist_val.append(ele[2])
            else: raise TypeError ("Unknown type of force or moment")
        elif len(ele)==4:       # If the load is Uniformly varying load.
            if isinstance(ele[0], (int, float)):
                h, b, a = abs(ele[0]-ele[1]), (ele[3]-ele[2]), min(ele[0],ele[1])
                equivalent_force=(ele[0]+ele[1])/2*(ele[3]-ele[2])
                if ele[1] > ele[0]:   # UVL with positive slope
                    cog = b/3*((3*a + 2*h)/(2*a + h)) + ele[2]
                elif ele[0] > ele[1]:   # UVL with negative slope
                    cog = b/3*((3*a + h)/(2*a + h)) + ele[2]
                elif ele[0] == ele[1]:  # Equivalent to UDL load.
                    raise ValueError ("Only three parameters are accepted for an UDL")
                ext_loads.append(equivalent_force)
                load_distances.append(cog)
                ext_moments.append(equivalent_force*cog)
                all_dist_val.extend([ele[2],ele[3]])
            elif ele[0]=='m':   # For distributed moments.
                equiv_moment = ele[1]*(ele[3] - ele[2])
                point_moments.append(equiv_moment)
                all_dist_val.extend([ele[2],ele[3]])
            else: raise TypeError ("Unknown type of force or moment")
        elif len(ele)==5:       # For Uniformly varying moment.
            if ele[0]=='m':
                equiv_moment = ((ele[1] + ele[2])/2)*(ele[4] - ele[3])
                point_moments.append(equiv_moment)
                all_dist_val.extend([ele[3],ele[4]])
            else: raise TypeError ("Unknown type of force or moment")
        else: raise TypeError ("Unknown type of force or moment")
                
    if support==(None,None): support = (0,length) # Default supports are at end oints.     
    all_dist_val.extend([support[0], support[1]])
    reaction_a = ((sum(ext_moments) - sum(ext_loads)*support[1] - sum(point_moments))
                                   /(support[0] - support[1]))
    reaction_b = sum(ext_loads) - reaction_a
    reactions =[reaction_a,reaction_b]
    delta_x = round(steps*length+1) # Total No. of steps of the beam.
    beam_length = [round(((length)/(delta_x-1)*i),5) for i in range(delta_x)]
    beam_height = [10 for i in beam_length] # X-Y coordinates for beam.
    unique_dist_vals = list(set(all_dist_val))
    for i in unique_dist_vals:     # To check if ext. load distances are present.
        if i not in beam_length: 
            beam_length.append(i)
            beam_length.sort()
            
    ld_y = [0 for i in range(len(beam_length))]
    for ele in forces:   # Getting the Y coordinates for load diagram.
        if len(ele)==2:
            id_val = beam_length.index(ele[1])
            ld_y[id_val] += -ele[0]
        elif len(ele)==3:
            if isinstance(ele[0], (int, float)):
                for i in range(beam_length.index(ele[1]),beam_length.index(ele[2])+1):
                    ld_y[i] += -ele[0]
            else : pass
        elif len(ele)==4 :
            if isinstance(ele[0], (int, float)):
                ix1, ix2 = beam_length.index(ele[2]), beam_length.index(ele[3])
                w1, w2, dw, L = ele[0], ele[1], (ele[1]-ele[0]), (ele[3]-ele[2])
                for i in range(ix1,ix2+1):
                    x = beam_length[i] - beam_length[ix1]
                    ld_y[i] += - (w1 + dw*(x/L))
                    
    ld_y[beam_length.index(support[0])] += reactions[0]
    ld_y[beam_length.index(support[1])] += reactions[1]

    sfd_y = [0 for i in range(len(beam_length))]
    for ele in forces:   # Getting the Y coordinates for shear force diagram.
        if len(ele)==2:
            ix = beam_length.index(ele[1])
            for num in range(ix,len(sfd_y)):
                sfd_y[num] += - ele[0]
        elif len(ele)==3:
            if isinstance(ele[0], (int, float)):
                ix1, ix2 = beam_length.index(ele[1]), beam_length.index(ele[2])
                L, w = (ele[2] - ele[1]), ele[0]
                for num in range(ix1,len(sfd_y)):
                    if num <= ix2+1:
                        x = (beam_length[num] - beam_length[ix1])
                        sfd_y[num] +=  - (w*x)
                    elif num > ix2+1:
                        sfd_y[num] += - (w*L)
            elif ele[0]=='m': pass  # Concentrated moments don't affect SFD.
        elif len(ele)==4:   # UVL loads are resonsible for parabolic SFD.
            if isinstance(ele[0], (int, float)):
                sfd_area = 0
                ix1 = beam_length.index(ele[2])
                ix2 = beam_length.index(ele[3])
                for num in range(ix1+1,ix2+1):
                    dx = round(beam_length[num] - beam_length[num-1],5)
                    dy = (ld_y[num-1] + ld_y[num])/2 
                    sfd_area += dy*dx
                    sfd_y[num] += sfd_area
                for num in range(ix2+1,len(sfd_y)):
                    sfd_y[num] += sfd_area
            elif ele[0]=='m': pass

    bmd_y = [0 for i in range(len(beam_length))]
    for ele in forces:
        if len(ele)==2:  # Point load
            ix = beam_length.index(ele[1])
            for num in range(ix,len(bmd_y)):
                x = beam_length[num] - beam_length[ix]
                bmd_y[num] += - (ele[0]*x)
        elif len(ele)==3:  
            if isinstance(ele[0], (int, float)): # Distributed load
                ix1, ix2 = beam_length.index(ele[1]), beam_length.index(ele[2])
                L, w = (ele[2] - ele[1]), ele[0]
                for num in range(ix1,ix2+1):
                    x = (beam_length[num] - beam_length[ix1])
                    bmd_y[num] += - (w*(x**2)/2)
                for num in range(ix2+1,len(bmd_y)):
                    x = (beam_length[num] - beam_length[ix1])
                    bmd_y[num] += - ((w*L/2)*(2*x - L))
            elif ele[0]=='m':  # Adding the effect of concentrated moments for BMD.
                ix = beam_length.index(ele[2])
                for num in range(ix,len(bmd_y)):
                    bmd_y[num] += - ele[1]
        elif len(ele)==4:   # UVL loads are resonsible for parabolic SFD.
            if isinstance(ele[0], (int, float)):
                ix1 = beam_length.index(ele[2])
                ix2 = beam_length.index(ele[3])
                h, L, w1 = abs(ele[0]-ele[1]), (ele[3]-ele[2]), min(ele[0],ele[1])
                for num in range(ix1,len(bmd_y)):
                    x = beam_length[num] - beam_length[ix1]
                    if ele[1] > ele[0]: # UVL with positive slope
                        if num <=ix2:   # Effect of UVL within its range
                            bmd_y[num] += - ((w1*(x**2)/2) + (h*(x**3)/(6*L)))
                        elif num > ix2: # Effect of UVL after its range
                            bmd_y[num] += - (((w1*L/2)*(2*x - L)) + ((h*L/2)*(x - (2*L/3))))
                    elif ele[0] > ele[1]: # UVL with negative slope
                        if num <=ix2:   # Effect of UVL within its range
                            bmd_y[num] += - ((w1*(x**2)/2) + (h*(x**3)/(3*L)))
                        elif num > ix2: # Effect of UVL after its range
                            bmd_y[num] += - (((w1*L/2)*(2*x - L)) + ((h*L/2)*(x - (L/3))))
                            
            elif ele[0]=='m':  # For the case of distributed moment.
                ix1 = beam_length.index(ele[2])
                ix2 = beam_length.index(ele[3])
                for num in range(ix1,len(bmd_y)):
                    x = beam_length[num] - beam_length[ix1]
                    if num <=ix2:   # Effect of DM within its span.
                        bmd_y[num] += - (ele[1]*x)
                    elif num > ix2: # Effect of DM after its span.
                        bmd_y[num] += - (ele[1]*(ele[3] - ele[2]))
                        
        elif len(ele)==5:
            if ele[0]=='m':   # For Uniformly varying moment.
                ix1 = beam_length.index(ele[3])
                ix2 = beam_length.index(ele[4])
                m1, dm = ele[1], (ele[2] - ele[1])
                L = (ele[4] - ele[3])
                for num in range(ix1,len(bmd_y)):
                    x = beam_length[num] - beam_length[ix1]
                    h = (m1 + (dm*(x/L)))
                    if num <=ix2:   # Effect of DM within its span.
                        bmd_y[num] += - (h*x)
                    elif num > ix2: # Effect of DM after its span.
                        bmd_y[num] += - ((m1 + (dm/2))*L)
                        
    for i in range(2):   # Taking the reactions for SFD & BMD.
        ix = beam_length.index(support[i])
        for num in range(ix,len(sfd_y)):
            x = beam_length[num] - beam_length[ix]
            sfd_y[num] += reactions[i]
            bmd_y[num] += reactions[i]*x

    def figure_plot (num, x, y, x_label=None,color=colors):
        plt.figure(num,figsize=(15,6))
        plt.plot(x, y, color[num-1])
        plt.plot([0,length],[0,0],ls='-.',lw=1,c='k')
        plt.xlabel(x_label)
        plt.grid(which='both')
        path = f'Figures/{x_label}' 
        plt.savefig(fname=path)

    figure_plot(1,beam_length,ld_y,'l_d')
    figure_plot(2,beam_length,sfd_y,'s_f_d')
    figure_plot(3,beam_length,bmd_y,'b_m_d')
   
   

    
# if __name__ == "__main__":
#     sfd_bmd_ssb(length=377,forces=[[35,34],[23,76],[23,45]])
