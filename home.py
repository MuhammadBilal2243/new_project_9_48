import subprocess
import tkinter as tk
# Create a window
root = tk.Tk()
root.title("My Shop")
def update_dollor():
    subprocess.Popen(["python", "dolor_rate.py"])
# Create a label for the title
title_label = tk.Label(root, text="Welcome to My Shop!", font=("Arial", 20, "bold"), pady=20)
title_label.pack()

# Create a frame for the buttons
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=20)

# Create a button for the inventory page
inventory_button = tk.Button(buttons_frame, text="View Inventory", width=15, height=2)
inventory_button.pack(side="left", padx=10)

# Create a button for the sales page
sales_button = tk.Button(buttons_frame, text="View Sales", width=15, height=2)
sales_button.pack(side="left", padx=10)

# Create a button for the customers page
customers_button = tk.Button(buttons_frame, text="View Customers", width=15, height=2)
customers_button.pack(side="left", padx=10)

# Create a button for the settings page
settings_button = tk.Button(buttons_frame, text="Settings", width=15, height=2)
settings_button.pack(side="left", padx=10)
# Create a button for the update_product page
update_product = tk.Button(buttons_frame, text="update_product", width=15, height=2)
update_product.pack(side="left", padx=10)
# Create a button for the expiry checking  page
product_expiry = tk.Button(buttons_frame, text="product_expiry", width=15, height=2)
product_expiry.pack(side="left", padx=10)
# Create a button for the update_dollor page
update_dollor = tk.Button(buttons_frame, text="update_dollor", width=15, height=2, command=update_dollor)
update_dollor.pack(side="left", padx=10)

# Create a frame for the status bar
status_frame = tk.Frame(root, bg="gray")
status_frame.pack(side="bottom", fill="x")

# Create a label for the shopping cart icon
cart_label = tk.Label(status_frame, text="🛒", font=("Arial", 16), bg="gray")
cart_label.pack(side="left", padx=10)

# Create a label for the total number of items in the shopping cart
cart_items_label = tk.Label(status_frame, text="0 items", font=("Arial", 12), bg="gray")
cart_items_label.pack(side="left", padx=10)

# Create a button for the shopping cart page
cart_button = tk.Button(status_frame, text="View Cart", width=10)
cart_button.pack(side="right", padx=10)

# Create a menu bar
menu_bar = tk.Menu(root)
# Create a "File" menu
file_menu = tk.Menu(menu_bar, tearoff=False)
file_menu.add_command(label="New", command=None)
file_menu.add_command(label="Open", command=None)
file_menu.add_separator()
file_menu.add_command(label="Exit", command=root.quit)
menu_bar.add_cascade(label="File", menu=file_menu)
# Create a "Help" menu
help_menu = tk.Menu(menu_bar, tearoff=False)
help_menu.add_command(label="About", command=None)
menu_bar.add_cascade(label="Help", menu=help_menu)

# Set the menu bar
root.config(menu=menu_bar)

# Start the main event loop
root.mainloop()