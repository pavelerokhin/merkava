import time
import tkinter as tk


def send_info_message(message):
    # Create the main window
    root = tk.Tk()
    root.title("MRKV: file updated")

    # Create a frame for better layout
    frame = tk.Frame(root, padx=20, pady=20)
    frame.pack()

    # Get OS information
    tk.Label(frame, text=message, font=("Helvetica", 14)).pack(pady=10)

    # Create a button to close the window
    tk.Button(frame, text="Ok", command=root.destroy).pack()

    # Run the GUI main loop
    root.mainloop()
