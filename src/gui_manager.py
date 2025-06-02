
import tkinter as tk
from tkinter import filedialog
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy


class GuiManager():
    def plot_fig(self, figure):
        for widget in self.pframe.winfo_children():
            widget.destroy()

        canvas = FigureCanvasTkAgg(figure, master=self.pframe)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    def create_fig(self, t, m):
        fig, ax = plt.subplots(figsize=(4, 8))
        ax.plot(t, m, label="Seismogram", linestyle="-", linewidth=0.5)
        ax.set_xlabel("Time [minutes]")
        ax.set_ylabel("Magnitude of Displacement")
        ax.set_title("Seismogram")
        ax.grid(True)
        return fig
    def open_file(self):
        f_path = filedialog.askopenfile(title="Select CSV to open", filetypes=[("All Files", "*"), ("CSV Files", ".csv")])
        if f_path:
            times, magnitude = self.process_file(f_path)
            if times is not None  and magnitude is not None:
                fig = self.create_fig(times, magnitude)
                self.plot_fig(fig)
    
    def process_file(self, path):
        df = pd.read_csv(path,  skiprows=4, header=None, dtype=str)
        df[0] = pd.to_datetime(df[0], errors="coerce")
        n_col = df.columns[1:]
        df[n_col] = df[n_col].apply(pd.to_numeric, errors='coerce')

        
        
        timestamps = ((df[0] - df.iloc[0, 0]).dt.total_seconds()) / 60
        magnitude = df.iloc[:, 5:].abs()
  
        if timestamps.empty and magnitude.empty:
            return None, None

        return timestamps, magnitude

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Sensor Report Replica")
        self.root.geometry("800x500")
        self.pframe = tk.Frame(self.root)
        self.pframe.pack(fill=tk.BOTH, expand=True)

        self._button = tk.Button(self.root, text="Open CSV", command=self.open_file).pack(pady=10)

                      

def main():
    manager = GuiManager()
    manager.root.mainloop()
if __name__ == "__main__":
    main()