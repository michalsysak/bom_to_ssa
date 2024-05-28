import re
import math
def read_txt_file(path):
    try:
        with open(path, 'r') as file:
            header = file.readline().strip().split(',')

            placements_list = []
            fid_list = []

            for line in file:
                values = line.strip().split()
                entry = dict(zip(header, values))
                if re.fullmatch(r'fid\d*', entry['Ref'], re.IGNORECASE):
                    fid_list.append(entry)
                else:
                    placements_list.append(entry)
            return placements_list, fid_list

    except FileNotFoundError:
        print("No such file or directory")
        return []

def write_ssa(file_path, placements):
    header = f'''[VERSION]

[PCB]
Unit System = MILIMETER
Coordinate = LOWER LEFT
Rotation = 0
Placement Origin = -560.000, 5.000 
Fiducial = CIRCLE, 8.062, -0.839, 544.970, 302.071
Accept Mark = NONE, 0, 0
Bad Mark = NONE, 0, 0

[BOARD]
Board Name = 
PCB Size = 560.000, 310.400, 3.000
Array = 1, 10, LOWER RIGHT
Array Offset = 0.000, 30.000

[PLACEMENTS]
'''

    placements_str = ''
    for placement in placements:
        placements_str += f'"{placement["Ref"]}" {placement["PlacementCentreX"]} {placement["PlacementCentreY"]} 0.000 {placement["Rotation"]} NONE 0 0 0 0 4286 0 "{placement["PartName"]}" "" ""\n'

    with open(file_path, 'w') as file:
        file.write(header + placements_str)

def unique_components(placements):
    return list(set(placement["PartName"] for placement in placements))

def find_closest_to_00(placements):
    min_distance = float('inf')
    closest_placement = None

    for placement in placements:
        x = float(placement["PlacementCentreX"])
        y = float(placement["PlacementCentreY"])
        distance = math.sqrt(x ** 2 + y ** 2)
        if distance < min_distance:
            min_distance = distance
            closest_placement = placement["Ref"]

    return closest_placement

def split_placements(placements, main_diode):

    #keep track of the placement times
    time_m1 = 0
    time_m2 = 0
    max_time_diff = 10
    placements_m1 = []
    placements_m2 = []

    #add none main diode components into m2
    placements_to_keep = []
    for placement in placements:
        if placement["PartName"] not in main_diode:
            time_m2 += 0.165
            placements_m2.append(placement)
            placements_to_keep.append(placement)

    # add the closest diode to placements_m1
    closest_00 = find_closest_to_00(placements_to_keep)
    for placement in placements_to_keep:
        if placement["Ref"] == closest_00:
            placements_m1.append(placement)
            time_m1 += 0.165
            break


    #assign the rest of diode components

    #print(placements_m1, end="\n")
    #print(placements_m2, end="\n")

    return placements_m1, placements_m2