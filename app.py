import customtkinter as ctk
from tkinter import filedialog, messagebox  # Import messagebox
import functions
import os
import re
import threading

class App(ctk.CTk):
    def __init__(self, root):
        self.root = root
        self.root.title("BOM to SSA Converter")
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")

        # Make the app static and define size
        self.root.resizable(False, False)
        self.root.geometry("600x800")
        self.initialize_variables()

        # Initialize fid_frame to None
        self.fid_frame = None

        # Create widgets
        self.create_widgets()

    def initialize_variables(self):
        # Initialize Variables with Default Values
        self.file_path = ctk.StringVar(value="")
        self.pcb_margin = ctk.DoubleVar(value=0.0)
        self.select_diode = ctk.StringVar(value="")
        self.select_fid1 = ctk.StringVar(value="")
        self.select_fid2 = ctk.StringVar(value="")
        self.pcb_size_x = ctk.DoubleVar(value=0.0)
        self.pcb_size_y = ctk.DoubleVar(value=0.0)
        self.pcb_size_z = ctk.DoubleVar(value=0.0)
        self.array_columns = ctk.IntVar(value=1)
        self.array_rows = ctk.IntVar(value=1)
        self.array_offset_x = ctk.DoubleVar(value=0.0)
        self.array_offset_y = ctk.DoubleVar(value=0.0)

        #only for manual fids
        self.manual_fid1_x = ctk.DoubleVar(value=0.0)
        self.manual_fid1_y = ctk.DoubleVar(value=0.0)
        self.manual_fid2_x = ctk.DoubleVar(value=0.0)
        self.manual_fid2_y = ctk.DoubleVar(value=0.0)

        # States variables
        self.are_fids = False
        self.file_selected = False

        # Placement variables
        self.placements_list = []
        self.fid_list = [] #only for the combobox

        self.components_list = []

    def clear_ui(self):
        for widget in self.root.winfo_children():
            widget.destroy()

    def create_widgets(self):
        self.clear_ui()
        self.create_header()
        self.create_file_section()
        self.create_pcb_section()
        self.create_fid_section()
        self.create_board_section()
        self.create_array_section()
        self.generate_button_progress()

    def create_header(self):
        # HEADER
        header_frame = ctk.CTkFrame(self.root, width=800, height=500)
        header_frame.grid(row=0, column=0, pady=10)
        header_label = ctk.CTkLabel(header_frame, text="BOM to SSA Converter", font=("Arial", 16), bg_color="#242424")
        header_label.pack()

    def create_file_section(self):
        # FILE SECTION
        file_frame = ctk.CTkFrame(self.root)
        file_frame.grid(row=1, column=0, pady=10)
        file_label = ctk.CTkLabel(file_frame, text="Upload TXT File", bg_color="#2b2b2b")
        file_label.grid(row=0, column=0, padx=10, pady=10)
        file_entry = ctk.CTkEntry(file_frame, textvariable=self.file_path, width=300)
        file_entry.grid(row=0, column=1, padx=5, pady=10)
        file_button = ctk.CTkButton(file_frame, text="Choose File", command=self.select_file)
        file_button.grid(row=0, column=2, padx=5, pady=10)

    def create_pcb_section(self):
        # PCB SECTION
        pcb_frame = ctk.CTkFrame(self.root, border_width=2, corner_radius=10)
        pcb_frame.grid(row=2, column=0, pady=10, padx=5, sticky="ew")
        pcb_margin_label = ctk.CTkLabel(pcb_frame, text="PCB Margin (mm)")
        pcb_margin_label.grid(row=0, column=0, padx=10, pady=(5, 2.5))
        pcb_margin_entry = ctk.CTkEntry(pcb_frame, textvariable=self.pcb_margin, validate="key",
                                        validatecommand=(self.root.register(self.validate_float), '%P'), width=175)
        pcb_margin_entry.grid(row=0, column=1, padx=10, pady=(5, 2.5))

        # Main diode
        self.select_diode_label = ctk.CTkLabel(pcb_frame, text="Main diode")
        self.select_diode_label.grid(row=3, column=0, padx=5, pady=(2.5, 5))
        self.select_diode_menu = ctk.CTkComboBox(pcb_frame, variable=self.select_diode, values=[], state='readonly',
                                                 width=175)
        self.select_diode_menu.grid(row=3, column=1, padx=5, pady=(2.5, 5))

    def create_fid_section(self):
        # Destroy the existing fid_frame if it exists
        if self.fid_frame is not None:
            self.fid_frame.destroy()

        # Create a new fid_frame
        self.fid_frame = ctk.CTkFrame(self.root, border_width=2, corner_radius=10)
        self.fid_frame.grid(row=3, column=0, pady=10, padx=5, sticky="ew")

        if self.file_selected:
            if self.are_fids:
                self.add_fid_combox()  # creates combobox for the fids in file
            else:
                self.add_fid_manual()   # creates manual entry for the fids
        else:
            no_fid_label = ctk.CTkLabel(self.fid_frame, text="No Fiducials found.")
            no_fid_label.grid(row=0, column=0, padx=15, pady=5, sticky="w")

    def add_fid_combox(self):
        self.fid_label = ctk.CTkLabel(self.fid_frame, text="Found fiducials:")
        self.fid_label.grid(row=0, column=0, padx=5, pady=2.5)

        self.select_fid_label1 = ctk.CTkLabel(self.fid_frame, text="Fiducial 1")
        self.select_fid_label1.grid(row=1, column=0, padx=5, pady=2.5)
        self.select_fid_entry1 = ctk.CTkComboBox(self.fid_frame, variable=self.select_fid1, values=[],
                                                 state='readonly', width=175)
        self.select_fid_entry1.grid(row=1, column=1, padx=5, pady=2.5)

        self.select_fid_label2 = ctk.CTkLabel(self.fid_frame, text="Fiducial 2")
        self.select_fid_label2.grid(row=2, column=0, padx=5, pady=2.5)
        self.select_fid_entry2 = ctk.CTkComboBox(self.fid_frame, variable=self.select_fid2, values=[],
                                                 state='readonly', width=175)
        self.select_fid_entry2.grid(row=2, column=1, padx=5, pady=2.5)

    def add_fid_manual(self):

        no_fid_label = ctk.CTkLabel(self.fid_frame, text="No Fiducials found. Please select manually:")
        no_fid_label.grid(row=0, column=0, padx=10, pady=2.5, sticky="w")

        # Frame for Fiducial 1
        fid1_frame = ctk.CTkFrame(self.fid_frame)
        fid1_frame.grid(row=1, column=0, padx=5, pady=2.5, sticky="w")

        self.no_fid1_label = ctk.CTkLabel(fid1_frame, text="Fiducial 1: ")
        self.no_fid1_label.pack(side="left", padx=10, pady=5)

        self.no_fid1_label_x = ctk.CTkLabel(fid1_frame, text="X: ")
        self.no_fid1_label_x.pack(side="left", padx=5, pady=2.5)
        self.no_fid1_label_x_entry = ctk.CTkEntry(fid1_frame, textvariable=self.manual_fid1_x, validate="key",
                                                  validatecommand=(self.root.register(self.validate_float), '%P'),
                                                  width=80)
        self.no_fid1_label_x_entry.pack(side="left", padx=5, pady=2.5)

        self.no_fid1_label_y = ctk.CTkLabel(fid1_frame, text="Y: ")
        self.no_fid1_label_y.pack(side="left", padx=5, pady=2.5)
        self.no_fid1_label_y_entry = ctk.CTkEntry(fid1_frame, textvariable=self.manual_fid1_y, validate="key",
                                                  validatecommand=(self.root.register(self.validate_float), '%P'),
                                                  width=80)
        self.no_fid1_label_y_entry.pack(side="left", padx=5, pady=2.5)

        # Frame for Fiducial 2
        fid2_frame = ctk.CTkFrame(self.fid_frame)
        fid2_frame.grid(row=2, column=0, padx=5, pady=2.5, sticky="w")

        self.no_fid2_label = ctk.CTkLabel(fid2_frame, text="Fiducial 2: ")
        self.no_fid2_label.pack(side="left", padx=10, pady=5)

        self.no_fid2_label_x = ctk.CTkLabel(fid2_frame, text="X: ")
        self.no_fid2_label_x.pack(side="left", padx=5, pady=2.5)
        self.no_fid2_label_x_entry = ctk.CTkEntry(fid2_frame, textvariable=self.manual_fid2_x, validate="key",
                                                  validatecommand=(self.root.register(self.validate_float), '%P'),
                                                  width=80)
        self.no_fid2_label_x_entry.pack(side="left", padx=5, pady=2.5)

        self.no_fid2_label_y = ctk.CTkLabel(fid2_frame, text="Y: ")
        self.no_fid2_label_y.pack(side="left", padx=5, pady=2.5)
        self.no_fid2_label_y_entry = ctk.CTkEntry(fid2_frame, textvariable=self.manual_fid2_y, validate="key",
                                                  validatecommand=(self.root.register(self.validate_float), '%P'),
                                                  width=80)
        self.no_fid2_label_y_entry.pack(side="left", padx=5, pady=2.5)

    def create_board_section(self):
        # BOARD SECTION
        board_frame = ctk.CTkFrame(self.root, border_width=2, corner_radius=10)
        board_frame.grid(row=4, column=0, pady=10, padx=5, sticky="ew")
        pcb_size_x_label = ctk.CTkLabel(board_frame, text="X Size")
        pcb_size_x_label.grid(row=0, column=0, padx=10, pady=(5, 2.5))
        pcb_size_x_entry = ctk.CTkEntry(board_frame, textvariable=self.pcb_size_x, validate="key",
                                        validatecommand=(self.root.register(self.validate_float), '%P'))
        pcb_size_x_entry.grid(row=0, column=1, padx=10, pady=2.5)
        pcb_size_y_label = ctk.CTkLabel(board_frame, text="Y Size")
        pcb_size_y_label.grid(row=1, column=0, padx=10, pady=2.5)
        pcb_size_y_entry = ctk.CTkEntry(board_frame, textvariable=self.pcb_size_y, validate="key",
                                        validatecommand=(self.root.register(self.validate_float), '%P'))
        pcb_size_y_entry.grid(row=1, column=1, padx=10, pady=2.5)
        pcb_size_z_label = ctk.CTkLabel(board_frame, text="Z Size")
        pcb_size_z_label.grid(row=2, column=0, padx=10, pady=2.5)
        pcb_size_z_entry = ctk.CTkEntry(board_frame, textvariable=self.pcb_size_z, validate="key",
                                        validatecommand=(self.root.register(self.validate_float), '%P'))
        pcb_size_z_entry.grid(row=2, column=1, padx=10, pady=(2.5, 5))

    def create_array_section(self):
        # Array widgets
        array_frame = ctk.CTkFrame(self.root, border_width=2, corner_radius=10)
        array_frame.grid(row=5, column=0, pady=5, padx=5, sticky="ew")
        array_columns_label = ctk.CTkLabel(array_frame, text="Columns")
        array_columns_label.grid(row=0, column=0, padx=5, pady=2.5)
        array_columns_entry = ctk.CTkEntry(array_frame, textvariable=self.array_columns, validate="key",
                                           validatecommand=(self.root.register(self.validate_int), '%P'))
        array_columns_entry.grid(row=0, column=1, padx=5, pady=2.5)
        array_rows_label = ctk.CTkLabel(array_frame, text="Rows")
        array_rows_label.grid(row=1, column=0, padx=5, pady=2.5)
        array_rows_entry = ctk.CTkEntry(array_frame, textvariable=self.array_rows, validate="key",
                                        validatecommand=(self.root.register(self.validate_int), '%P'))
        array_rows_entry.grid(row=1, column=1, padx=5, pady=2.5)

        array_offset_frame = ctk.CTkFrame(self.root, border_width=2, corner_radius=10)
        array_offset_frame.grid(row=6, column=0, pady=5, padx=5, sticky="ew")
        offset_x_label = ctk.CTkLabel(array_offset_frame, text="Array Offset X")
        offset_x_label.grid(row=0, column=0, padx=5, pady=2.5)
        offset_x_entry = ctk.CTkEntry(array_offset_frame, textvariable=self.array_offset_x, validate="key",
                                      validatecommand=(self.root.register(self.validate_float), '%P'))
        offset_x_entry.grid(row=0, column=1, padx=5, pady=2.5)
        offset_y_label = ctk.CTkLabel(array_offset_frame, text="Array Offset Y")
        offset_y_label.grid(row=1, column=0, padx=5, pady=2.5)
        offset_y_entry = ctk.CTkEntry(array_offset_frame, textvariable=self.array_offset_y, validate="key",
                                      validatecommand=(self.root.register(self.validate_float), '%P'))
        offset_y_entry.grid(row=1, column=1, padx=5, pady=2.5)

    def generate_button_progress(self):
        # Generate button widget
        generate_frame = ctk.CTkFrame(self.root, width=400, height=200)
        generate_frame.grid(row=7, column=0, pady=20)
        generate_button = ctk.CTkButton(generate_frame, text="Generate Files", width=250, command=self.generate_files)
        generate_button.pack(pady=10)

        # Progress bar widget
        self.progress = ctk.CTkProgressBar(generate_frame, orientation="horizontal", width=350, height=10,
                                           mode="determinate")
        self.progress.pack(padx=10, pady=10)
        self.progress.set(0)

    def select_file(self):
        try:
            self.progress.set(0)
            self.file_path.set(filedialog.askopenfilename(filetypes=[("Text files", "*.txt")]))

            self.placements_list, self.fid_list = functions.read_txt_file(self.file_path.get())
            unique_components = functions.unique_components(self.placements_list)

            if unique_components:
                self.select_diode_menu.configure(values=unique_components)
                self.select_diode.set(unique_components[0])
            if len(self.fid_list) >= 2:
                self.are_fids = True
            else:
                self.are_fids = False
                messagebox.showinfo("No Fiducials found",
                                    f"No Fiducials found in {self.file_path.get()}. Please select manually")

            self.file_selected = True

            # Update the fiducial section dynamically after the state variables are set
            self.create_fid_section()

            if self.are_fids:
                # Set the fid values
                fid_values = [f"{fid['Ref']} X:{fid['PlacementCentreX']} Y:{fid['PlacementCentreY']}" for fid in
                              self.fid_list]
                self.select_fid_entry1.configure(values=fid_values)
                self.select_fid_entry2.configure(values=fid_values)
                self.select_fid1.set(fid_values[0])
                self.select_fid2.set(fid_values[1])

        except Exception as e:
            print(f"Error: {e}")

    def validate_input(self):
        errors = []

        if not self.file_path.get():
            errors.append("File path is empty")

        if self.pcb_margin.get() <= 0.0:
            self.pcb_margin.set(0)
            errors.append("PCB margin must be greater than 0")

        if self.pcb_size_x.get() <= 0.0:
            self.pcb_size_x.set(0)
            errors.append("PCB X size must be greater than 0")
        if self.pcb_size_y.get() <= 0.0:
            self.pcb_size_y.set(0)
            errors.append("PCB Y size must be greater than 0")
        if self.pcb_size_z.get() <= 0.0:
            self.pcb_size_z.set(0)
            errors.append("PCB Z size must be greater than 0")

        if self.array_columns.get() <= 0:
            self.array_columns.set(1)
            errors.append("Array columns set to default value 1")

        if self.array_rows.get() <= 0:
            self.array_rows.set(1)
            errors.append("Array rows set to default value 1")

        if self.array_offset_x.get() < 0.0:
            self.array_offset_x.set(0)
            errors.append("Array offset X must be greater than 0")
        if self.array_offset_y.get() < 0.0:
            self.array_offset_y.set(0)
            errors.append("Array offset Y must be greater than 0")

        # Display all errors in one pop-up if there are any
        if errors:
            messagebox.showerror("Input Error", "\n".join(errors))
            return False

        messagebox.showinfo("Files Created", "All Files Created")
        return True

    def validate_float(self, value_allowed):
        if value_allowed in ('', '-', '.', '-.', '0.', '-0.'):
            return True
        try:
            float(value_allowed)
            return True
        except ValueError:
            return False

    def validate_int(self, value_allowed):
        if value_allowed == '':
            return True
        try:
            int(value_allowed)
            return True
        except ValueError:
            return False

    def generate_files(self):
        self._update_progress(0)  # Ensure the progress bar starts at 0
        thread = threading.Thread(target=self._generate_files_task)
        thread.start()

    def _generate_files_task(self):
        try:
            self._update_progress(0)
            if not self.validate_input():
                self._update_status("Validation failed, please correct the input fields.")
                return

            self._update_progress(0.1)

            file1_path = os.path.splitext(self.file_path.get())[0] + "_M1.ssa"
            file2_path = os.path.splitext(self.file_path.get())[0] + "_M2.ssa"

            array_number = self.array_rows.get() * self.array_columns.get()
            file1_placements, file2_placements = functions.split_placements(
                self.placements_list, self.select_diode.get(), array_number)
            self._update_progress(0.3)

            pcb = {
                'x': self.pcb_size_x.get(),
                'y': self.pcb_size_y.get(),
                'z': self.pcb_size_z.get(),
                'margin': self.pcb_margin.get()
            }
            if self.are_fids:
                fid1 = re.sub(r'[XY]:', '', self.select_fid1.get()[4:]).split(' ')
                fid2 = re.sub(r'[XY]:', '', self.select_fid2.get()[4:]).split(' ')
                fiducials = [
                    {'name': self.select_fid1.get()[:4], 'x': fid1[1], 'y': fid1[2]},
                    {'name': self.select_fid2.get()[:4], 'x': fid2[1], 'y': fid2[2]}
                ]
            else:
                fiducials = [
                    {'name': "FID1", "x": self.manual_fid1_x.get(), "y": self.manual_fid1_y.get()},
                    {'name': "FID2", "x": self.manual_fid2_x.get(), "y": self.manual_fid2_y.get()}
                ]
            self._update_progress(0.5)

            array = {
                'columns': self.array_columns.get(),
                'rows': self.array_rows.get(),
                'offsetX': self.array_offset_x.get(),
                'offsetY': self.array_offset_y.get()
            }
            self._update_progress(0.6)

            functions.write_ssa(file1_path, file1_placements, pcb, fiducials, array)
            self._update_progress(0.8)
            functions.write_ssa(file2_path, file2_placements, pcb, fiducials, array)
            self._update_progress(1.0)

            self._update_status("Files Created")

        except Exception as e:
            self._update_status(f"Error: {e}")
            self._update_progress(0)

    def _update_progress(self, progress):
        self.root.after(0, lambda: self.progress.set(progress))
        self.root.after(0, self.root.update_idletasks)

    def _update_status(self):
        self.root.after(0, self.root.update_idletasks)


if __name__ == "__main__":
    root = ctk.CTk()
    app = App(root)
    root.mainloop()
