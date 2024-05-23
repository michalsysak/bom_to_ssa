import tkinter as tk
from tkinter import filedialog
from tkinter import messagebox
def select_existing_file():
    file_path = filedialog.askopenfilename()
    if file_path:
        label_existing.config(text=f"Selected Existing File: {file_path}")
        show_loading_screen()
        # Simulate a loading process
        threading.Thread(target=simulate_loading, args=(file_path,)).start()

def select_new_file_path():
    file_path = filedialog.asksaveasfilename()
    if file_path:
        label_new.config(text=f"Selected New File Path: {file_path}")
        show_loading_screen()
        # Simulate a loading process
        threading.Thread(target=simulate_loading, args=(file_path,)).start()

def simulate_loading(file_path):
    time.sleep(2)  # Simulate a loading time of 2 seconds
    hide_loading_screen()

def show_loading_screen():
    canvas.pack(pady=10)
    root.update()

def hide_loading_screen():
    canvas.pack_forget()
    root.update()
def main():

    # Create the main window
    root = tk.Tk()
    root.title("File Selector")
    root.geometry("400x400")

    # Create a frame to organize widgets
    frame = tk.Frame(root)
    frame.pack(pady=20)

    # Create a label and button for selecting an existing file
    label_existing = tk.Label(frame, text="No existing file selected")
    label_existing.grid(row=0, column=0, padx=10, pady=10)
    button_existing = tk.Button(frame, text="Select Existing File", command=select_existing_file)
    button_existing.grid(row=1, column=0, padx=10, pady=10)

    # Create a label and button for selecting a new file path
    label_new = tk.Label(frame, text="No new file path selected")
    label_new.grid(row=0, column=1, padx=10, pady=10)
    button_new = tk.Button(frame, text="Select New File Path", command=select_new_file_path)
    button_new.grid(row=1, column=1, padx=10, pady=10)

    # Create a canvas for the loading screen with an arrow
    canvas = tk.Canvas(root, width=100, height=100)
    canvas.create_line(10, 50, 90, 50, arrow=tk.LAST)  # Draw an arrow

    # Initially hide the loading screen
    canvas.pack_forget()

    # Run the application
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
