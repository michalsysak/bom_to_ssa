import re
import gui
def read_txt_file(path):
    # read from txt to a dictionary
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

def write_ssa(file_path, placements, fid_list):
    #add margin
    header = '''[VERSION]

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

def main():
    #placement_list, fid_list = read_txt_file("indeks_programu.txt")
    app = gui.App()
    app.mainloop()

if __name__ == '__main__':
    main()
