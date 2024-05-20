import tkinter as tk
def main():

    root = tk.Tk()
    root.title("bom_to_ssa")

    data_dict = read_txt_file("indeks_programu.txt")
    print(write_ssa(data_dict))
    root.mainloop()
def read_txt_file(path):
    # read from txt to a dictionary
    try:
        with open(path, 'r') as file:
            header = file.readline().strip().split(',')

            data_list = []

            for line in file:
                values = line.strip().split()
                entry = dict(zip(header, values))
                data_list.append(entry)

    except FileNotFoundError:
        print("No such file or directory")
    return data_list

def write_ssa(placements):
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

    with open('indeks_programu.ssa', 'w') as file:
        file.write(header + placements_str)

if __name__ == '__main__':
    main()
