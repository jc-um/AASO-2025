
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy


class GuiManager():
    def plot_fig(self, figure):
        pass
    def create_fig(self):
        pass
    def open_file(self):
        f_path = filedialog.askopenfile(title="Select CSV to open", filetypes=[("All Files", "*"), ("CSV Files", ".csv")])
        if f_path:
            times, magnitude = self.process_file(f_path)
            if times != None and magnitude != None:
                fig = self.create_fig()
                self.plot_fig(fig)
    
    def process_file(self, path):
        df = pd.read_csv(path,  skiprows=4, header=None, dtype=str)
        df[0] = pd.to_datetime(df[0], errors="coerce")
        n_col = df.columns[1:]
        df[n_col] = df[n_col].apply(pd.to_numeric, errors='coerce')
        shape = df.shape
        r = shape[0]
        
        
        df["TIME_DIFF"] = ((df[0] - df.iloc[0, 0]).dt.total_seconds()) / 60
        c = df.columns.get_loc("TIME_DIFF")
        
        print(df["TIME_DIFF"])
        
        df.iloc[:, 5:c]= df.iloc[:, 5:c].apply(lambda  col : numpy.linalg.norm(col), axis=0)
                                                                                                                 
        df.to_csv("gui_test.csv", index=False, header=True)
        return df["TIME_DIFF"], df.iloc[:, 5:c]

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