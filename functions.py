import re
import math
import os
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

def write_ssa(file_path, placements, pcb, fiducials, array):

    header = f'''[VERSION]

[PCB]
Unit System = MILIMETER
Coordinate = LOWER LEFT
Rotation = 0
Placement Origin = -{pcb['x']}, {pcb['margin']} 
Fiducial = CIRCLE, {fiducials[0]['x']}, {fiducials[0]['y']}, {fiducials[1]['x']}, {fiducials[1]['y']}
Accept Mark = NONE, 0, 0
Bad Mark = NONE, 0, 0

[BOARD]
Board Name = {os.path.splitext(os.path.basename(file_path))[0]}
PCB Size = {pcb['x']}, {pcb['y']+0.4}, 3.000
Array = {array['columns']}, {array['rows']}, LOWER RIGHT
Array Offset = {array['offsetX']}, {array['offsetY']}

[PLACEMENTS]
'''
    placements_str = ''
    for placement in placements:
        placements_str += f'"{placement["Ref"]}" {placement["PlacementCentreX"]} {placement["PlacementCentreY"]} 0.000 {placement["Rotation"]} NONE 0 0 0 0 4286 0 "{placement["PartName"]}" "" ""\n'

    with open(file_path, 'w') as file:
        file.write(header + placements_str)

def unique_components(placements):
    return list(set(placement["PartName"] for placement in placements))

def split_placements(placements, main_diode, array_number):

    # Keep track of the placement times
    time_m1 = 0
    time_m2 = 0
    placements_m1 = []
    placements_m2 = []

    #time diff value to change if you want different time diffs
    min_time_diff = 8

    # Add non-main diode components into m2
    placements_to_keep = []
    for placement in placements:
        if placement["PartName"] not in main_diode:
            time_m2 += 0.165 * array_number
            placements_m2.append(placement)
        else:
            placements_to_keep.append(placement)

    # Assign the rest of the diode components
    i = 0
    while i < len(placements_to_keep):
        if time_m1 <= time_m2 + min_time_diff:
            placements_m1.append(placements_to_keep[i])
            placements_to_keep.pop(i)
            time_m1 += 0.160 * array_number
        else:
            placements_m2.append(placements_to_keep[-i-1])
            placements_to_keep.pop(-i-1)
            time_m2 += 0.165 * array_number

    print(time_m1, time_m2)
    return placements_m1, placements_m2
