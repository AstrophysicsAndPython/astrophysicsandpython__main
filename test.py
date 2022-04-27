"""
Created on Apr 19 00:33:42 2022
"""


def magnitude_with_separate_direction(magnitude, direction, starting_position=0):
    if direction == 'negative':
        position = starting_position - magnitude
    else:
        position = starting_position + magnitude

    print(f'The starting position of the object is {starting_position}.\n'
          f'With a magnitude of {magnitude} and a {direction} direction, '
          f'the current position is {position}.')

    return position
