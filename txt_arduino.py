# For communication
codereader = 'code.txt'

file_handle = open(codereader, "r")
text = file_handle.read().splitlines()
line_items = [line.split() for line in text]
function, angle_values, distance_values, speed_values = zip(*line_items)
