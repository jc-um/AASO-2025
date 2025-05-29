import pandas as pd


class Cleaner():
    def __init__(self, f_path):
        self._path = f_path
        self._df = pd.read_csv(self.f_path, header=None, dtype=str)
    
    def clean_data(self, output_path="", max_magnitude=100):
        self._df[0] = pd.to_datetime(self._df[0], errors="coerce")

        self._df.dropna(inplace=True)
        self._df.drop_duplicates(subset=[0])

        n_col = self._df.columns[1:]
        self._df[n_col] = self._df[n_col].apply(pd.to_numeric, errors='coerce')

        
        
        
