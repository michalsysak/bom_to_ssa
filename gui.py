import tkinter as tk
from tkinter import filedialog
import os
class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("BOM to SSA")
        self.geometry("800x600") #window size

        self.create_widgets()

    def create_widgets(self):
        # Create frames
        self.header = tk.Frame(self, bg='lightblue', height=100)
        self.content = tk.Frame(self, bg='white')
        self.footer = tk.Frame(self, bg='black', height=20)

        # Layout frames
        self.header.grid(row=0, column=0, columnspan=2, sticky="ew")
        self.content.grid(row=1, column=1, sticky="nsew")
        self.footer.grid(row=2, column=0, columnspan=2, sticky="ew")

        # Configure grid for resizing
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # Configure the content frame grid for no stretching on the first row and column
        self.content.grid_columnconfigure(0, weight=0)
        self.content.grid_rowconfigure(0, weight=0)

        # Add widgets to the header
        tk.Label(self.header, text="BOM to SSA converter for SMT", bg='lightblue').pack(side="left")

        # File selection button in the content
        self.file_button = tk.Button(self.content, text="Select BOM File", command=self.open_file_dialog)
        self.file_button.grid(row=0, column=0, sticky="nw", padx=10, pady=10)

        # Label to display selected file path in the content
        self.file_label_bom = tk.Label(self.content, text="No file selected", bg='white')
        self.file_label_bom.grid(row=1, column=0, padx=10, pady=10)

    def open_file_dialog(self):
        filepath = filedialog.askopenfilename(
            title="Select BOM file",
            filetypes=(("Text files", "*.txt"), ("All files", "*.*"))
        )
        if filepath:
            filename = os.path.basename(filepath)
            print("Selected file:", filepath)  # Handle the file path as needed
            self.file_label_bom.config(text=f"Current file: {filename}")  # Update the label with the file path

if __name__ == "__main__":
    app = App()
    app.mainloop()