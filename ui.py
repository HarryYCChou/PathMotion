from loader import load_data
from analyzer import get_description, get_sensor_data
from simulator import simulate
from plot import plot_result
import pandas as pd
import tkinter as tk
from tkinter import ttk, filedialog
import threading

# Initialize tkinter UI
root = tk.Tk()
root.title("Path Motion Simulation")
root.geometry("600x160") 

# Global Parameters
file_path = ""

def update_progress(value, processing_item="Unknown"):
    progress['value'] = value
    root.update_idletasks()  # Refresh the UI
    progress_label.config(text=f"{value:.2f}% {processing_item}")

def check_thread(thread):
    if thread.is_alive():
        root.after(100, check_thread, thread)
    else:
        print("Thread finished")

def on_browse_file_button_click():
    global file_path
    file_path = filedialog.askopenfilename(
        title="Select a File",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )
    if file_path:  # Check if a file was selected
        file_label.config(text=f"Selected File: {file_path}")
        simulate_button.config(state=tk.NORMAL)

def threaded_load_data_and_simulate(file_path, update_progress):
    raw_data = load_data(file_path, update_progress)
    if raw_data is not None:
        #print("Data loaded successfully!")
        #print("Load data description...")
        description = get_description(raw_data)
        time_data, accel_data_low, accel_data_high, gyro_data = get_sensor_data(raw_data)
        # update description label
        test_date_label.config(text=f"Test Date: {description['test_date']}")
        test_time_label.config(text=f"Test Time: {description['test_time']}")
        sample_rate_label.config(text=f"Sample Rate: {description['sample_rate']}")
        #file_label.config(text=f"Selected File: {file_path}")
        #print("Run simulation...")
        result = simulate(accel_data_high.to_numpy().astype(float),
                          gyro_data.to_numpy().astype(float),
                          1/int(description['sample_rate']), update_progress)
        #print("Plot result...")
        plot_result(result)
    else:
        print("Invalid file path or format")

def on_simulate_button_click():
    # disable simulate button
    simulate_button.config(state=tk.DISABLED)
    # Start the loading thread
    thread = threading.Thread(target=threaded_load_data_and_simulate, args=(file_path, update_progress))
    thread.start()
    # Check the thread's status
    root.after(100, check_thread, thread)  # Keep checking

# toolbar frame
toolbar_frame = tk.Frame(root, width=300, height=40)
toolbar_frame.pack(side=tk.TOP, padx=10, fill=tk.X)

# description frame
desc_frame = tk.Frame(root, width=300, height=40)
desc_frame.pack(padx=10, fill=tk.X)

# progress frame
prog_frame = tk.Frame(root, width=300, height=40)
prog_frame.pack(padx=10, fill=tk.X)

# browse file button
browse_file_button = tk.Button(toolbar_frame, text="Select file", command=on_browse_file_button_click)
browse_file_button.pack(side=tk.LEFT, padx=10, pady=10)  # Position the button with some padding

# simulate button
simulate_button = tk.Button(toolbar_frame, text="Simulate", command=on_simulate_button_click, state=tk.DISABLED)
simulate_button.pack(side=tk.LEFT, padx=10, pady=10)  # Position the button with some padding

# Label to display the selected file path
file_label = tk.Label(desc_frame, anchor=tk.W, text="Selected File: No file selected")
file_label.pack(fill=tk.X)

# Label to display the selected file path
test_date_label = tk.Label(desc_frame, anchor=tk.W, text="Test Date: ")
test_date_label.pack(fill=tk.X)

# Label to display the selected file path
test_time_label = tk.Label(desc_frame, anchor=tk.W, text="Test Time: ")
test_time_label.pack(fill=tk.X)

# Label to display the selected file path
sample_rate_label = tk.Label(desc_frame,anchor=tk.W, text="Sample Rate: ")
sample_rate_label.pack(fill=tk.X)

# progress bar
progress = ttk.Progressbar(prog_frame, orient="horizontal", length=300, mode="determinate")
progress.pack(side=tk.LEFT)

# Label to display the progress
progress_label = tk.Label(prog_frame, anchor=tk.W, text="100% ")
progress_label.pack(padx=10, fill=tk.X)

def start_ui():
    root.mainloop()