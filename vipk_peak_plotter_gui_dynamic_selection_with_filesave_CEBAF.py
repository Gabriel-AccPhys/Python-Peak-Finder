# See the README file first!
# Plotting and Peak Detection Tool
# Gabriel Palacios gabrielp@jlab.org	 05/09/2025

# This project benefited from assistance provided by OpenAI's ChatGPT, utilizing the GPT-4-turbo model. 
# The AI was employed as a tool to support code development, data visualization, user interface design, and documentation tasks.
# ==============================


import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import find_peaks
from tkinter import Tk, filedialog, Checkbutton, IntVar, Label, Button, Entry, Toplevel
from datetime import datetime

def load_and_plot():
    # File selection
    root = Tk()
    root.withdraw()
    file_path = filedialog.askopenfilename(title="Select data file", filetypes=[("CSV/TXT files", "*.csv *.txt")])
    if not file_path:
        print("No file selected.")
        return

    # Try reading with whitespace or comma delimiter
    try:
        df = pd.read_fwf(file_path)
    except Exception:
        df = pd.read_csv(file_path)

    df = df.replace('?', pd.NA).dropna()
    if 'Date' not in df.columns:
        print("No 'Date' column found in the file.")
        return

    df['Date'] = pd.to_datetime(df['Date'], errors='coerce')
    df = df.dropna(subset=['Date'])

    # Parse numeric columns
    for col in df.columns:
        if col != 'Date':
            df[col] = pd.to_numeric(df[col], errors='coerce')
    df = df.dropna()

    # Filter out clearly invalid VIPK values
    vipk_cols = [col for col in df.columns if col.startswith('VIP')]
    for col in vipk_cols:
        df = df[df[col] < 10]

    # GUI for signal selection
    selection_win = Toplevel()
    selection_win.title("Signal Selector")

    signal_vars = {}
    for i, col in enumerate(df.columns):
        if col != 'Date':
            var = IntVar(value=1 if col.startswith('VIP') else 0)
            chk = Checkbutton(selection_win, text=col, variable=var)
            chk.grid(row=i, column=0, sticky='w')
            signal_vars[col] = var

    Label(selection_win, text="Peak Height (e.g. 5e-6):").grid(row=0, column=1)
    height_entry = Entry(selection_win)
    height_entry.insert(0, "5e-6")
    height_entry.grid(row=0, column=2)

    Label(selection_win, text="Peak Prominence (e.g. 5e-6):").grid(row=1, column=1)
    prom_entry = Entry(selection_win)
    prom_entry.insert(0, "5e-6")
    prom_entry.grid(row=1, column=2)

    def submit_selection():
        selected = [col for col, var in signal_vars.items() if var.get() == 1]
        try:
            height_val = float(height_entry.get())
            prom_val = float(prom_entry.get())
        except ValueError:
            print("Invalid peak parameters.")
            selection_win.destroy()
            return

        peak_kwargs = {'height': height_val, 'prominence': prom_val}
        selection_win.destroy()
        plot_selected_signals(df, selected, peak_kwargs)

    Button(selection_win, text="Plot", command=submit_selection).grid(row=len(df.columns)+1, column=0, columnspan=3)
    selection_win.mainloop()

def plot_selected_signals(df, selected_signals, peak_kwargs):
    time = df['Date']
    peak_data = []

    fig, ax1 = plt.subplots(figsize=(12, 6))
    ax2 = ax1.twinx()

    color_cycle = plt.rcParams['axes.prop_cycle'].by_key()['color']
    color_map = {name: color_cycle[i % len(color_cycle)] for i, name in enumerate(selected_signals)}

    for name in selected_signals:
        signal = df[name]
        color = color_map[name]

        if name.startswith('VIP'):
            ax1.plot(time, signal / 1e-6, label=name, color=color)
            peaks, _ = find_peaks(signal, **peak_kwargs)
            ax1.plot(time.iloc[peaks], signal.iloc[peaks] / 1e-6, 'o', color=color, label=f'{name} Peaks')

            for i in peaks:
                t = time.iloc[i]
                val = signal.iloc[i] / 1e-6
                ax1.annotate(f'{val:.2f}', (t, val), textcoords="offset points", xytext=(-20, -10),
                             ha='center', fontsize=8, rotation=45, color=color)
                peak_data.append({'Channel': name, 'Time': t, 'Value (uA)': val})
        else:
            ax2.plot(time, signal / 1e3, label=name, linestyle='--', color=color)

    ax1.set_xlabel('Time')
    ax1.set_ylabel('VIP Currents (uA)')
    ax2.set_ylabel('Voltages (kV)')
    ax1.tick_params(axis='y')
    ax2.tick_params(axis='y')

    lines1, labels1 = ax1.get_legend_handles_labels()
    lines2, labels2 = ax2.get_legend_handles_labels()
    ax1.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

    plt.title('Signal Plot with Peak Detection')
    plt.grid(True)
    plt.tight_layout()

    # Save CSV BEFORE showing plot
    if peak_data:
        date_str = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        output_filename = f"Detected_Peaks_{date_str}.csv"
        pd.DataFrame(peak_data).to_csv(output_filename, index=False)
        print(f"Saved peak data to '{output_filename}'.")

    plt.show()

if __name__ == "__main__":
    load_and_plot()
