"""
Created on Wed Mar 24 18:19:25 2021
"""

import error_utilities as e_utils


class NumberLine:
    """
    NumberLine class deals with some number line functionalities. These include

    1- magnitude_without_direction
    2- magnitude_with_direction
    3- magnitude_with_separate_direction

    
    """

    def __init__(self, magnitude: float, starting_position: float = 0):
        self.magnitude = magnitude
        self.start = starting_position

    def magnitude_without_direction(self):
        if not isinstance(self.magnitude, float):
            raise e_utils.FloatNotPassed('Parameter type should be of float type.')

        if self.magnitude < 0:
            raise e_utils.MagnitudeIsLessThanZero('Magnitude cannot be less than 0.')

        positive_position = self.start + self.magnitude
        negative_position = self.start - self.magnitude

        print(f'The starting position is {self.start}.\n'
              f'With no direction specified, the object can have either '
              f'{negative_position} or {positive_position} position.')

        return [positive_position, negative_position]

    def magnitude_with_direction(self):
        if not isinstance(self.magnitude, float):
            raise e_utils.FloatNotPassed('Parameter type should be of float type.')

        obj_position = self.start + self.magnitude

        print(f'The starting position of the object is {self.start}.\n With a '
              f'magnitude of {self.magnitude}, the final position of the object is '
              f'{obj_position}.')

        return obj_position

    def magnitude_with_separate_direction(self, direction: str):
        if not isinstance(self.magnitude, float):
            raise e_utils.FloatNotPassed('Parameter type should be of float type.')

        if self.magnitude < 0:
            print('Magnitude cannot be negative with a given direction, assuming '
                  'positive')
            self.magnitude = abs(self.magnitude)

        if direction not in ['positive', 'negative']:
            raise e_utils.DirectionIsNotPosNeg('Direction should be positive or negative')

        if direction == 'negative':
            pos = self.start - self.magnitude
        else:
            pos = self.start + self.magnitude

        print(f'The starting position of the object is {self.start}.\n'
              f'With a magnitude of {self.magnitude} and a {direction} direction, '
              f'the current position is {pos}.')

        return pos
