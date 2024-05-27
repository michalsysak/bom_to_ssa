import tkinter as tk
from tkinter import filedialog, ttk
import functions
import os

class App(tk.Tk):
    def __init__(self, root):
        self.root = root
        self.root.title("BOM to SSA Converter")

        # Variables
        self.file_path = tk.StringVar()
        self.pcb_margin = tk.DoubleVar()
        self.select_diode = tk.StringVar(value="")
        self.select_fid1 = tk.StringVar(value="")
        self.select_fid2 = tk.StringVar(value="")
        self.pcb_size_x = tk.DoubleVar()
        self.pcb_size_y = tk.DoubleVar()
        self.pcb_size_z = tk.DoubleVar()
        self.array_columns = tk.IntVar()
        self.array_rows = tk.IntVar()
        self.offset_x = tk.DoubleVar()
        self.offset_y = tk.DoubleVar()

        self.placements_list = []
        self.fid_list = []
        self.components_list = []

        self.create_widgets()

    def create_widgets(self):
        # HEADER
        header_frame = tk.Frame(self.root)
        header_frame.pack(pady=10)
        header_label = tk.Label(header_frame, text="BOM to SSA Converter", font=("Arial", 16))
        header_label.pack()

        # FILE SECTION
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10)
        file_label = tk.Label(file_frame, text="Upload TXT File")
        file_label.grid(row=0, column=0, padx=5)
        file_entry = tk.Entry(file_frame, textvariable=self.file_path, width=50)
        file_entry.grid(row=0, column=1, padx=5)
        file_button = tk.Button(file_frame, text="Choose File", command=self.select_file)
        file_button.grid(row=0, column=2, padx=5)

        # PCB SECTION
        pcb_frame = tk.LabelFrame(self.root, text="PCB")
        pcb_frame.pack(pady=10, fill="x", padx=5)
        pcb_margin_label = tk.Label(pcb_frame, text="PCB Margin(mm)")
        pcb_margin_label.grid(row=0, column=0, padx=5)
        pcb_margin_entry = tk.Entry(pcb_frame, textvariable=self.pcb_margin)
        pcb_margin_entry.grid(row=0, column=1, padx=5)

        # fiducials
        self.select_fid_label1 = tk.Label(pcb_frame, text="Fiducial1 ")
        self.select_fid_label1.grid(row=1, column=0, padx=5)
        self.select_fid_entry1 = ttk.Combobox(pcb_frame, textvariable=self.select_fid1, state='readonly')
        self.select_fid_entry1.grid(row=1, column=1, padx=5)

        self.select_fid_label2 = tk.Label(pcb_frame, text="Fiducial2 ")
        self.select_fid_label2.grid(row=2, column=0, padx=5)
        self.select_fid_entry2 = ttk.Combobox(pcb_frame, textvariable=self.select_fid2, state='readonly')
        self.select_fid_entry2.grid(row=2, column=1, padx=5)

        # main diode
        self.select_diode_label = tk.Label(pcb_frame, text="Main diode")
        self.select_diode_label.grid(row=3, column=0, padx=5)
        self.select_diode_menu = ttk.Combobox(pcb_frame, textvariable=self.select_diode, state='readonly')
        self.select_diode_menu.grid(row=3, column=1, padx=5)

        # BOARD SECTION
        board_frame = tk.LabelFrame(self.root, text="BOARD")
        board_frame.pack(pady=10, fill="x", padx=5)
        pcb_size_frame = tk.LabelFrame(board_frame, text="PCB Size (mm)")
        pcb_size_frame.pack(pady=5, fill="x", padx=5)
        pcb_size_x_label = tk.Label(pcb_size_frame, text="X Size")
        pcb_size_x_label.grid(row=0, column=0, padx=5)
        pcb_size_x_entry = tk.Entry(pcb_size_frame, textvariable=self.pcb_size_x)
        pcb_size_x_entry.grid(row=0, column=1, padx=5)
        pcb_size_y_label = tk.Label(pcb_size_frame, text="Y Size")
        pcb_size_y_label.grid(row=1, column=0, padx=5)
        pcb_size_y_entry = tk.Entry(pcb_size_frame, textvariable=self.pcb_size_y)
        pcb_size_y_entry.grid(row=1, column=1, padx=5)
        pcb_size_z_label = tk.Label(pcb_size_frame, text="Z Size")
        pcb_size_z_label.grid(row=2, column=0, padx=5)
        pcb_size_z_entry = tk.Entry(pcb_size_frame, textvariable=self.pcb_size_z)
        pcb_size_z_entry.grid(row=2, column=1, padx=5)

        #Array widgets
        array_frame = tk.LabelFrame(board_frame, text="Array Configuration")
        array_frame.pack(pady=5, fill="x", padx=5)
        array_columns_label = tk.Label(array_frame, text="Columns")
        array_columns_label.grid(row=0, column=0, padx=5)
        array_columns_entry = tk.Entry(array_frame, textvariable=self.array_columns)
        array_columns_entry.grid(row=0, column=1, padx=5)
        array_rows_label = tk.Label(array_frame, text="Rows")
        array_rows_label.grid(row=1, column=0, padx=5)
        array_rows_entry = tk.Entry(array_frame, textvariable=self.array_rows)
        array_rows_entry.grid(row=1, column=1, padx=5)

        array_offset_frame = tk.LabelFrame(board_frame, text="Array Offset (mm)")
        array_offset_frame.pack(pady=5, fill="x", padx=5)
        offset_x_label = tk.Label(array_offset_frame, text="Offset X")
        offset_x_label.grid(row=0, column=0, padx=5)
        offset_x_entry = tk.Entry(array_offset_frame, textvariable=self.offset_x)
        offset_x_entry.grid(row=0, column=1, padx=5)
        offset_y_label = tk.Label(array_offset_frame, text="Offset Y")
        offset_y_label.grid(row=1, column=0, padx=5)
        offset_y_entry = tk.Entry(array_offset_frame, textvariable=self.offset_y)
        offset_y_entry.grid(row=1, column=1, padx=5)

        #generate button widget
        generate_frame = tk.Frame(self.root)
        generate_frame.pack(pady=10)
        generate_button = tk.Button(generate_frame, text="Generate Files", command=self.generate_files)
        generate_button.pack()

        #Progress bar widget
        self.progress = ttk.Progressbar(generate_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

    def select_file(self):
        self.file_path.set(filedialog.askopenfilename(filetypes=[("Text files", "*.txt")])) #open file
        self.placements_list, self.fid_list = functions.read_txt_file(self.file_path.get()) #get placement list and fid list
        unique_components = functions.unique_components(self.placements_list) #get unique components
        self.select_diode_menu['values'] = unique_components #assign to the ui

        if unique_components:
            self.select_diode.set(unique_components[0])

        if self.fid_list:
            fid_values = [f"{fid['Ref']}: X: {fid['PlacementCentreX']} Y: {fid['PlacementCentreY']}" for fid in self.fid_list]
            self.select_fid_entry1['values'] = fid_values
            self.select_fid_entry2['values'] = fid_values
            self.select_fid1.set(fid_values[0])
            self.select_fid2.set(fid_values[0])

    def generate_files(self):
        #get the path for the new files
        file1_path = os.path.splitext(self.file_path.get())[0] + "_M1.ssa"
        file2_path = os.path.splitext(self.file_path.get())[0] + "_M2.ssa"

        file1_placements, file2_placements = functions.split_placements(self.placements_list, self.select_diode.get())

        functions.write_ssa(file1_path, file1_placements)
        functions.write_ssa(file2_path, file2_placements)

        self.progress['value'] = 0
        self.root.update_idletasks()
        for i in range(5):
            self.progress['value'] += 20
            self.root.update_idletasks()
            self.root.after(500)

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()
