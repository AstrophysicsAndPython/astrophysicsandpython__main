"""
Created on Thu Mar 24 09:06:45 2021

"""

import error_utilities as e_utils


def distance_formula(final_coordinates, initial_coordinates=(0, 0, 0)):
    """
    Provides Euclidean distance between two points in 3 or less dimensional space.

    Parameters
    ----------
    final_coordinates :
        position of the object in the space under observation
    initial_coordinates :
        reference coordinates according to which the distance is to be calculated.
        Default is (0,0,0).

    Returns
    -------
    distance :
        Euclidean distance between the two specified points

    Notes
    -------
        To use distance_formula_3d for 2D, specify z as 0 in both lists or only give 2
    element list.

    """

    # check that the final_coordinates passed are either a list/tuple,
    if not isinstance(final_coordinates, list) or isinstance(final_coordinates, tuple):
        raise e_utils.ListNotGiven('Must be either a list or tuple.')

    # check and correct the length of the list/tuple passed
    if len(final_coordinates) < 3:
        final_coordinates = e_utils.check_list_len_3d(final_coordinates)

    # convert to an immutable object
    final_coordinates = tuple(final_coordinates)

    # initialize
    x1, y1, z1 = initial_coordinates
    x2, y2, z2 = final_coordinates

    # calculate the components
    del_x = (x2 - x1)**2
    del_y = (y2 - y1)**2
    del_z = (z2 - z1)**2

    # return the result
    return (del_x + del_y + del_z)**0.5
