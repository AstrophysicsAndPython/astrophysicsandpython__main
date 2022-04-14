"""
Created on Wed Mar 24 18:19:25 2021
"""

import errors.errors__the_number_line as err


class NumberLine:
    """
    NumberLine class deals with some number line functionalities. These include

    1- magnitude_without_direction
    2- magnitude_with_direction
    3- magnitude_with_separate_direction

    
    """

    def __init__(self, magnitude: float, starting_position: float = 0):
        self.magnitude = magnitude
        self.starting_position = starting_position

    def magnitude_without_direction(self):
        if not isinstance(self.magnitude, float):
            raise err.FloatNotPassed('Parameter type should be of float type.')

        if self.magnitude < 0:
            raise err.MagnitudeIsLessThanZero('Magnitude cannot be less than 0.')

        obj_position_positive = self.starting_position + self.magnitude
        obj_position_negative = self.starting_position - self.magnitude

        print(f'The starting position is {self.starting_position}.\n'
              f'With no direction specified, the object can have either {obj_position_negative} or {obj_position_positive} position.')

        return [obj_position_positive, obj_position_negative]

    def magnitude_with_direction(self):
        if not isinstance(self.magnitude, float):
            raise err.FloatNotPassed('Parameter type should be of float type.')

        obj_position = self.starting_position + self.magnitude

        print(
            f'The starting position of the object is {self.starting_position}.\n With a magnitude of '
            f'{self.magnitude}, the final position of the object is {obj_position}.')

        return obj_position

    def magnitude_with_separate_direction(self, direction: str):
        if not isinstance(self.magnitude, float):
            raise err.FloatNotPassed('Parameter type should be of float type.')

        if self.magnitude < 0:
            raise err.MagnitudeIsLessThanZero('Magnitude cannot be less than 0.')

        if direction not in ['positive', 'negative']:
            raise err.DirectionIsNotPosNeg('Direction can either be positive or negative only.')

        obj_position = self.starting_position - self.magnitude if direction == 'negative' else self.starting_position + self.magnitude

        print(f'The starting position of the object is {self.starting_position}.\n'
              f'With a magnitude of {self.magnitude} and a {direction} direction, the current position is {obj_position}.')

        return obj_position
