import math
from txt_reader import *

y_1 = 0
x_1 = 0

r = []
theta = []
y_coordinates = []
x_coordinates = []
time_values = []


# the list called time_values will be used to calculate how long it will take to get the next coordinates.
# So consider each time_values's unit as second.

class Calculate(Reader):
    @classmethod
    def calculate(cls):
        print(*cls.read())
        values = cls.read()
        angle_values = values[0]
        distance_values = values[1]
        speed_values = values[2]
        v = []

        r = []

        theta = []

        for i in angle_values:
            radiant_value = int(i) * math.pi / 180
            theta.append(radiant_value)

        for j in distance_values:
            r.append(int(j))

        for k in speed_values:
            v.append(int(k))

        return r, theta, v


"""
As you see on code.txt there is multiple "move value_1 value_2 value_3". So each time car moves, code always use the 
next values. The code.txt can have more an less than 6 lines so that's why I create lists for coordinates.
"""
