# For simulation app
codereader = 'code.txt'


class Reader:
    codereader = 'code.txt'

    @classmethod
    def read(klass):
        print("Reading Instructions...")
        with open(klass.codereader, "r") as file_handle:
            text = file_handle.read().splitlines()
            line_items = [line.split() for line in text]
            function, angle_values, distance_values, speed_values = zip(*line_items)
            return angle_values, distance_values, speed_values


'''
These are the values we're going to use on the simulations.
angle unit = degree
distance unit = cm
speed unit = cm/s
'''