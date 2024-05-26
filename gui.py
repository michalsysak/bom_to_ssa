import tkinter as tk
from tkinter import filedialog, ttk
class App(tk.Tk):
    def __init__(self, root):
        self.root = root
        self.root.title("BOM to SSA Converter")

        # Variables
        self.file_path = tk.StringVar()
        self.pcb_margin = tk.DoubleVar()
        self.select_option = tk.StringVar(value="Option 1")
        self.pcb_size_x = tk.DoubleVar()
        self.pcb_size_y = tk.DoubleVar()
        self.pcb_size_z = tk.DoubleVar()
        self.array_columns = tk.IntVar()
        self.array_rows = tk.IntVar()
        self.offset_x = tk.DoubleVar()
        self.offset_y = tk.DoubleVar()

        self.create_widgets()

    def create_widgets(self):
        # Header
        header_frame = tk.Frame(self.root)
        header_frame.pack(pady=10)
        header_label = tk.Label(header_frame, text="TXT to SSA Converter", font=("Arial", 16))
        header_label.pack()

        # File input section
        file_frame = tk.Frame(self.root)
        file_frame.pack(pady=10)
        file_label = tk.Label(file_frame, text="Upload TXT File")
        file_label.grid(row=0, column=0, padx=5)
        file_entry = tk.Entry(file_frame, textvariable=self.file_path, width=50)
        file_entry.grid(row=0, column=1, padx=5)
        file_button = tk.Button(file_frame, text="Choose File", command=self.select_file)
        file_button.grid(row=0, column=2, padx=5)

        # PCB Section
        pcb_frame = tk.LabelFrame(self.root, text="PCB")
        pcb_frame.pack(pady=10, fill="x", padx=5)
        pcb_margin_label = tk.Label(pcb_frame, text="PCB Margin")
        pcb_margin_label.grid(row=0, column=0, padx=5)
        pcb_margin_entry = tk.Entry(pcb_frame, textvariable=self.pcb_margin)
        pcb_margin_entry.grid(row=0, column=1, padx=5)
        select_option_label = tk.Label(pcb_frame, text="Select Option")
        select_option_label.grid(row=1, column=0, padx=5)
        select_option_menu = ttk.Combobox(pcb_frame, textvariable=self.select_option, values=["Option 1", "Option 2"])
        select_option_menu.grid(row=1, column=1, padx=5)

        # BOARD Section
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

        # Generate Section
        generate_frame = tk.Frame(self.root)
        generate_frame.pack(pady=10)
        generate_button = tk.Button(generate_frame, text="Generate Files", command=self.generate_files)
        generate_button.pack()

        self.progress = ttk.Progressbar(generate_frame, orient="horizontal", length=300, mode="determinate")
        self.progress.pack(pady=10)

    def select_file(self):
        self.file_path.set(filedialog.askopenfilename(filetypes=[("Text files", "*.txt")]))

    def generate_files(self):
        self.progress['value'] = 0
        self.root.update_idletasks()
        for i in range(5):
            self.progress['value'] += 20
            self.root.update_idletasks()
            self.root.after(500)

# Run the application
if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()