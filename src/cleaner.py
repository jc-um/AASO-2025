import pandas as pd
import sys

if len(sys.argv) != 2:
    raise RuntimeError("(PROGRAM FAILURE) Must input (2) arguments ")

class Cleaner():
    def __init__(self, f_path):
        self._path = f_path
        self._df = pd.read_csv(self._path, skiprows=4, header=None, dtype=str)
        self._df.to_csv("initial.csv", index=False)
    def clean_data(self, output_path="", max_magnitude=100):
        self._df[0] = pd.to_datetime(self._df[0], errors="coerce")

        self._df.replace("", float("NaN"), inplace=True)

        self._df.dropna(how='all', axis=1, inplace=True)
        self._df.drop_duplicates(subset=[0], inplace=True)

        n_col = self._df.columns[1:]
        self._df[n_col] = self._df[n_col].apply(pd.to_numeric, errors='coerce')

        self._df = self._df.loc[:, (self._df != self._df.iloc[0]).any()]
        self._df = self._df.set_index(0).resample('h').ffill(limit=10).bfill(limit=10).reset_index()
        
        self._df[n_col] = self._df[n_col].interpolate(method="linear")
        #self._df = self._df.reset_index() 

        self._df.iloc[:, 5:] *= 0.6
        initial_data = self._df.iloc[0, 5:]
        
        s = self._df.shape
        r = s[0]
        c = s[1]
        print(s)
        
        self._df.to_csv("clean.csv", index=False)     
        for i in range(0, r):
            for j in range(5, c):
                
                initial = initial_data[j]

                curr = self._df.iloc[i, j]

                displacement = curr - initial
                
                self._df.iloc[i, j] = displacement
        
        if output_path == "":
            ext = self._path.rfind(".")
            output_path = self._path[:ext] + "_cleaned.csv"
            print(f"Saved to {output_path}")
        self._df.to_csv(output_path, index=False)            

def main():
    data_cleaner = Cleaner(sys.argv[1])
    data_cleaner.clean_data()
    
if __name__ == "__main__":
    main()
