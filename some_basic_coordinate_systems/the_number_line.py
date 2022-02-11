"""
Created on Wed Mar 24 18:19:25 2021
"""

import errors.error_base as eb
import errors.error_messages as em


class NumberLine:

    def __init__(self, magnitude: int, starting_position: int = 0):
        self.magnitude = magnitude
        self.starting_position = starting_position

    def number_line_with_direction(self):
        try:

            if type(self.magnitude) != int:
                raise eb.IntNotPassed

            obj_position = self.starting_position + self.magnitude

            print(f'The starting position of the object is {self.starting_position}.\n With a magnitude of {self.magnitude}, the final position of the object is {obj_position}.')

            return obj_position

        except eb.IntNotPassed:
            em.IntNotPassed()

    def number_line_no_direction(self):
        try:

            if type(self.magnitude) != int:
                raise eb.IntNotPassed

            if self.magnitude < 0:
                raise eb.MagnitudeIsLessThanZero

            obj_position_positive = self.starting_position + self.magnitude
            obj_position_negative = self.starting_position - self.magnitude

            print(f'The starting position is {self.starting_position}.\n'
                  f'With no direction specified, the object can have either {obj_position_negative} or {obj_position_positive} position.')

            return [obj_position_positive, obj_position_negative]

        except eb.IntNotPassed:
            em.IntNotPassed()

        except eb.MagnitudeIsLessThanZero:
            em.MagnitudeIsLessThanZero()

    def number_line_separate_direction(self, direction: str):
        try:

            if type(self.magnitude) != int:
                raise eb.IntNotPassed

            if self.magnitude < 0:
                raise eb.MagnitudeIsLessThanZero

            if direction not in ['positive', 'negative']:
                raise eb.DirectionIsNotPosNeg

            if direction == 'negative':
                obj_position = self.starting_position - self.magnitude

            else:
                obj_position = self.starting_position + self.magnitude

            print(f'The starting position of the object is {self.starting_position}.\n'
                  f'With a magnitude of {self.magnitude} and a {direction} direction, the current position is {obj_position}.')

            return obj_position

        except eb.IntNotPassed:
            em.IntNotPassed()

        except eb.MagnitudeIsLessThanZero:
            em.MagnitudeIsLessThanZero()

        except eb.DirectionIsNotPosNeg:
            em.DirectionIsNotPosNeg()
