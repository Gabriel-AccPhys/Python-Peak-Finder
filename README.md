# Python-Peak-Finder
==============================
README: Plotting and Peak Detection Tool
Gabriel Palacios gabrielp@jlab.org	 05/09/2025

This project benefited from assistance provided by OpenAI's ChatGPT, utilizing the GPT-4-turbo model. The AI was employed as a tool to support code development, data visualization, user interface design, and documentation tasks.
==============================

This tool allows users to:
- Load and analyze a data file containing current and voltage signals.
- Select which channels to plot using a graphical interface.
- Detect and annotate peaks in selected current signals.
- Save a CSV file containing detailed peak data.

==============================
User Instructions
==============================

1. **Prepare Your Data File**
   - Ensure your file is formatted correctly (fixed-width or tab-delimited).
   - The file must contain a 'Date' column with parseable datetime strings.
   - The file must include one or more numeric columns such as VIPK201cur, VIPK202cur, etc.

2. **Run the Script**
   - Double-click the `.exe` file (on Windows) or run the `.py` file from a terminal:
     ```
     python your_script_name.py
     ```

3. **Select Channels to Plot**
   - A window will appear showing a list of checkboxes for available channels.
   - Check the boxes for the current and voltage signals you wish to plot.

4. **Adjust Peak Detection Settings**
   - Enter `height` and `prominence` values for peak detection (use scientific notation if needed, e.g., `5e-6`).
   - These settings determine which peaks are detected based on amplitude and sharpness.

5. **View the Plot**
   - The selected signals are plotted over time.
   - Detected peaks are marked and labeled on the graph.

6. **View Output Files**
   - As soon as the plot is generated, a CSV file is saved in the same folder.
   - The file contains a list of detected peaks and their associated timestamps and signal names.
   - The filename includes the date and time of execution.

==============================
Requirements
==============================

To run the script from source, make sure the following Python packages are installed:

- `pandas`
- `matplotlib`
- `scipy`

You can install them with pip:
```
pip install pandas matplotlib scipy
```

Python version 3.7 or later is recommended.

==============================
Known Limitations and Tips
==============================

1. **File Format Issues**
   - Make sure the file structure is clean and includes all expected columns.

2. **Date Parsing Errors**
   - Standardize date formats before using the script if you encounter parsing issues.

3. **Peak Detection Configuration**
   - Use reasonable values for `height` and `prominence` to ensure meaningful peaks are detected.

4. **Color Assignment Conflicts**
   - With many signals, colors may repeat. Interpretation becomes harder.

5. **Axes Overlap and Plot Clutter**
   - Avoid selecting too many signals at once if readability is important.

6. **Missing Dependencies or Environment Errors**
   - Install required Python packages if running the script from source:
     ```
     pip install pandas matplotlib scipy
     ```

7. **GUI and Display Issues**
   - The script uses `tkinter`, which may not work on some remote/headless systems.

==============================
General Recommendation
==============================
Always test with a sample dataset before full-scale use. Provide clean inputs and validate peak detection visually.
. 
