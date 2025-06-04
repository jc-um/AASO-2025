import tkinter as tk
from tkinter import filedialog, messagebox
import csv
import pandas as pd
import io

# === Selectors ===
def select_dat_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.askopenfilename(title="Select the .dat file", filetypes=[("DAT Files", "*.dat")])

def select_output_file():
    root = tk.Tk()
    root.withdraw()
    return filedialog.asksaveasfilename(title="Save Final Cleaned CSV As", defaultextension=".csv", filetypes=[("CSV Files", "*.csv")])

# === Step 1: Convert .dat to list of rows ===
def convert_dat_to_list(dat_file):
    with open(dat_file, 'r', newline='') as infile:
        reader = csv.reader(infile, delimiter=',')
        return list(reader)

# === Step 2: Remove formatting rows ===
def remove_formatting_rows(row_list):
    if len(row_list) > 0:
        row_list.pop(0)  # remove top row
    saved_row = row_list[0] if len(row_list) > 0 else None
    for i in sorted([2, 1], reverse=True):
        if i < len(row_list):
            del row_list[i]
    return row_list, saved_row

# === Step 3: Keep only relevant columns ===
def keep_specific_columns(row_list):
    buffer = io.StringIO()
    writer = csv.writer(buffer)
    writer.writerows(row_list)
    buffer.seek(0)

    required_columns = ['TIMESTAMP', 'RECORD', 'Batt_volt', 'PTemp', 'TransactionID3'] + \
        [f"GF_Readings3({i},{j})" for i in range(1, 30) for j in range(1, 4 + 1)]

    df = pd.read_csv(buffer, dtype=str, on_bad_lines='skip')  # treat everything as str
    df = df.loc[:, df.columns.intersection(required_columns)]
    df = df.reindex(columns=required_columns)
    return df

# === Step 4: Drop incomplete rows using user's logic ===
def remove_incomplete_rows_custom(df):
    # Redefine all known missing indicators as NaN
    df.replace(["NAN", "NaN", "n/a", "N/A", "", " "], pd.NA, inplace=True)
    original_count = len(df)
    df_cleaned = df.dropna(thresh=7)
    removed = original_count - len(df_cleaned)
    return df_cleaned, removed

# === Full Pipeline ===
def main():
    dat_path = select_dat_file()
    if not dat_path:
        return

    out_path = select_output_file()
    if not out_path:
        return

    try:
        rows = convert_dat_to_list(dat_path)
        rows, saved_row = remove_formatting_rows(rows)
        df = keep_specific_columns(rows)
        df_cleaned, removed_count = remove_incomplete_rows_custom(df)
        df_cleaned.to_csv(out_path, index=False)

        messagebox.showinfo(
            "Success",
            f"Final cleaned file saved to:\n{out_path}\n\nSaved Row: {saved_row}\nRows removed: {removed_count}"
        )
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred:\n{e}")

if __name__ == "__main__":
    main()
