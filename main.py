import tkinter as tk
from tkinter import messagebox, filedialog, scrolledtext
import webbrowser

from lib import mt5

def export_orders():
    result = mt5Obj.Export()
    if result[0] != 0:
        log_message(result[1])
        log_message(f"The export file path : {result[0]}")
    else:
        messagebox.showwarning("Info", result[1])

def import_orders():
    file_path = filedialog.askopenfilename(
        title="Select a Export File",
        filetypes=(("CSV files", "*.csv"), ("All files", "*.*"))
    )
    if file_path:
        log_message(f"File selected: {file_path}\n")
        result = mt5Obj.Import(file_path)
        for item in result:
            log_message(item)
    else:
        messagebox.showwarning("No File Selected", "No file was selected.")
        log_message("No file selected.")

def show_about():
    about_message = (
        "This software was created by Qasem Talaee.\n\n"
        "For more information, visit my website:\n"
        "https://tradeqt.com\n\n"
        "Also you can see my github:\n"
        "https://github.com/qasem-talaee"
    )
    result = messagebox.showinfo("About Me", about_message)
    if result == "ok":
        webbrowser.open("https://tradeqt.com")

def log_message(message):
    log_text.config(state=tk.NORMAL)
    log_text.insert(tk.END, message + "\n")
    log_text.config(state=tk.DISABLED)
    log_text.yview(tk.END)

def clear_log():
    log_text.config(state=tk.NORMAL)
    log_text.delete(1.0, tk.END)
    log_text.config(state=tk.DISABLED)

root = tk.Tk()
root.title("MT5 Export & Import")

window_width = 600
window_height = 500

screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x = (screen_width // 2) - (window_width // 2)
y = (screen_height // 2) - (window_height // 2)
root.geometry(f"{window_width}x{window_height}+{x}+{y}")

title_label = tk.Label(root, text="MT5 Export and Import Limit Orders", font=("Arial", 16, "bold"), fg="blue")
title_label.pack(pady=10)

button_frame = tk.Frame(root)
button_frame.pack(pady=10)

message_button = tk.Button(button_frame, text="Export Orders", command=export_orders)
message_button.pack(side=tk.LEFT, padx=5)

file_button = tk.Button(button_frame, text="Import Orders", command=import_orders)
file_button.pack(side=tk.LEFT, padx=5)

clear_button = tk.Button(button_frame, text="Clear Log", command=clear_log)
clear_button.pack(side=tk.LEFT, padx=5)

about_button = tk.Button(button_frame, text="About", command=show_about)
about_button.pack(side=tk.LEFT, padx=5)

log_frame = tk.Frame(root)
log_frame.pack(fill=tk.BOTH, expand=True, pady=10)

scrollbar = tk.Scrollbar(log_frame)
scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

log_text = tk.Text(log_frame, wrap=tk.WORD, state=tk.DISABLED, yscrollcommand=scrollbar.set)
log_text.pack(fill=tk.BOTH, expand=True)

scrollbar.config(command=log_text.yview)

mt5Obj = mt5.MT5()
init = mt5Obj.initialize()
if init[0] == 0:
    messagebox.showinfo("Error", init[1])
    log_message(init[1])
else:
    log_message(init[1])

root.mainloop()
mt5Obj.shutdown()