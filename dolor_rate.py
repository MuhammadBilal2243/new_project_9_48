
import tkinter as tk
import mysql.connector
from tkinter import ttk

# Create a connection to the MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bilal123",
    database="testno10"
)

# Define a function to update the rate value in the database
def update_rate(rate):
    cursor = conn.cursor()
    sql = "UPDATE pkr SET rate = %s WHERE id = 1"
    val = (rate,)
    cursor.execute(sql, val)
    conn.commit()

# Define a function to fetch the rate value from the database
def fetch_rate():
    cursor = conn.cursor()
    sql = "SELECT rate FROM pkr WHERE id = 1"
    cursor.execute(sql)
    result = cursor.fetchone()
    return result

# Define a function to handle the "Update" button click
def update_button_click():
    new_rate = float(rate_entry.get())
    update_rate(new_rate)
    rate_label["text"] = fetch_rate()

# Create the main window
root = tk.Tk()

# Create the style for the GUI controls
style = ttk.Style(root)

style.configure("TLabel", font=("Segoe UI", 20), padding=(5, 5, 5, 5))
style.configure("TEntry", font=("Segoe UI", 20))
style.configure("TButton", font=("Segoe UI", 20))

# Create the GUI controls
rate_label = ttk.Label(root, text=fetch_rate())
rate_label.grid(row=0, column=1)
rl = ttk.Label(root, text="Current rate:")
rl.grid(row=0, column=0, sticky="W")

ral = ttk.Label(root, text="New rate:")
ral.grid(row=1, column=0, sticky="W")
rate_entry = ttk.Entry(root, width=10,font=("Segoe UI", 20))
rate_entry.grid(row=1, column=1, columnspan=4, padx=5)

update_button = ttk.Button(root, text="Update", command=update_button_click)
update_button.grid(row=2, column=0, padx=5, pady=10)

# Set the padding for the root window and expand it
root.geometry("300x150")
root.minsize(300,150)
root.rowconfigure(3, weight=1)
root.columnconfigure(1, weight=1)
root.configure(padx=10, pady=10)

# Start the GUI loop
root.mainloop()