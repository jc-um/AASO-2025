
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class GuiManager():
    def plot_fig(self, figure):
        pass
    def create_fig(self):
        pass
    def open_file(self):
        f_path = filedialog.askopenfile(title="Select CSV to open", filetypes=[("All Files", "*"), ("CSV Files", ".csv")])
        if f_path:
            times, magnitude = self.process_file(f_path)
            if times and magnitude:
                fig = self.create_fig()
                self.plot_fig(fig)
    
    def process_file(self, path):
        df = pd.read_csv(path, header=None)
        df[0] = pd.to_datetime(df[0], errors="coerce")
        shape = df.shape
        r = shape[0]

        df["TIME_DIFF"] = ((df[0] - df.iloc[0, 0]).dt.total_seconds()) / 60
        
        print(df["TIME_DIFF"])
       
        df.to_csv("gui_test.csv", index=False, header=True)


    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sensor Report Replica")
        self.root.geometry("800x500")

        self._button = tk.Button(self.root, text="Open CSV", command=self.open_file).pack(pady=10)

                      

def main():
    manager = GuiManager()
    manager.root.mainloop()
if __name__ == "__main__":
    main()