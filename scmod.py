"""
science module for ships.

version of the 20180613.
"""

import numpy as np

def from_orbital_to_cartesian_coordinates(a, e, inc, RAAN, om, t, mu):
    '''
    Converting from orbital parameters to cartesian coordinates.
    - Inputs:
            a         float   semi-major axis (km)
    		e         float   eccentricity (-)
    		inc       float   inclination (deg)
    		RAAN      float   right ascension of the ascending node (deg)
    		om        float   argument of periapsis (deg)
    		t         float   time spent since passage at periapsis (s)
    		mu	      float   gravitational parameter of the central body	(km3/s2)
    - Outputs:
    		pos   	  numpy array of floats (shape (3,)) (km) (! y, z, x)
    '''

    # converting angles from degrees to radians
    inc = inc * np.pi / 180
    RAAN = RAAN * np.pi / 180
    om = om * np.pi / 180

    # computing mean anomaly
    n = np.sqrt(mu / np.power(a, 3.0))
    M = n * t

    # computing eccentric anomaly
    E = [M]
    for j in range(100):
        E.append(E[j] + (M - E[j] + e * np.sin(E[j])) / (1 - e * np.cos(E[j])))
        if(abs(E[j+1] - E[j]) < 1e-8):
            E = E[j+1]
            break

    # computing true anomaly
    nu = 2 * np.arctan2(
            np.sqrt(1 - e) * np.cos(E / 2),
            np.sqrt(1 + e) * np.sin(E / 2)
        ) % (np.pi * 2)

    # computing radius
    r = a * (1 -np.power(e, 2.0)) / (1 + e * np.cos(nu))

    # computing position vector
    pos = np.asarray((
        r * (np.cos(om + nu) * np.sin(RAAN) - np.sin(om + nu) * np.cos(RAAN) * np.cos(inc)),
        r * (np.sin(om + nu) * np.sin(inc)),
        r * (np.cos(om + nu) * np.cos(RAAN) - np.sin(om + nu) * np.sin(RAAN) * np.cos(inc))
    ))

    return pos

def rotate_frame_around_z(input_vector, angle):
    '''
	Converts coordinates to rotated reference frame.
    Inputs:
    -input_vector       numpy array of floats
    -angle (degrees)    float
    Outputs:
    -output_vector      numpy array of floats
    '''

    angle = angle * np.pi / 180

    output_vector = [
        np.cos(angle) * input_vector[0] - np.sin(angle) * input_vector[1],
        np.sin(angle) * input_vector[0] + np.cos(angle) * input_vector[1],
        input_vector[2]
    ]

    return output_vector

def rotate_frame_around_y(input_vector, angle):
    '''
	Converts coordinates to rotated reference frame.
    Inputs:
    -input_vector       numpy array of floats
    -angle (degrees)    float
    Outputs:
    -output_vector      numpy array of floats
    '''

    angle = angle * np.pi / 180

    output_vector = [
        np.cos(angle) * input_vector[0] + np.sin(angle) * input_vector[2],
        input_vector[1],
        np.cos(angle) * input_vector[2] - np.sin(angle) * input_vector[0]
    ]

    return output_vector
