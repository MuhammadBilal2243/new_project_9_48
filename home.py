import subprocess
import tkinter as tk
# Create a window
root = tk.Tk()
root.title("My Shop")

def inventory_button():
    subprocess.Popen(["python", "customer_invoice.py"])
def search_order_by_no():
    subprocess.Popen(["python", "order_details.py"])

def update_dollor():
    subprocess.Popen(["python", "dolor_rate.py"])
def updateProduct():
    subprocess.Popen(["python", "update_products.py"])
def Enter_new_products():
    subprocess.Popen(["python", "new_product_entery.py"])
def Custumer_orders():
    subprocess.Popen(["python","customer_orders_detail.py"])
def orders_datails():
    subprocess.Popen(["python", "order_details.py"])
# Create a label for the title
title_label = tk.Label(root, text="Welcome to My Shop!", font=("Arial", 20, "bold"), pady=20)
title_label.pack()

# Create a frame for the buttons
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=20)

# Create a button for the inventory page
inventory_button = tk.Button(buttons_frame, text="View Inventory", width=15, height=2,command=inventory_button)
inventory_button.pack(side="left", padx=10)

# Create a button for the sales page
sales_button = tk.Button(buttons_frame, text="View Sales", width=15, height=2)
sales_button.pack(side="left", padx=10)

# Create a button for the customers page
customers_button = tk.Button(buttons_frame, text="View Customers", width=15, height=2)
customers_button.pack(side="left", padx=10)

# Create a button for the settings    page
orders_datails_button = tk.Button(buttons_frame, text="Enter new products", width=25, height=2,command=Enter_new_products)
orders_datails_button.pack(side="left", padx=10)
# Create a button for the update_product page
update_product = tk.Button(buttons_frame, text="update_product", width=15, height=2,command=updateProduct)
update_product.pack(side="left", padx=10)
# Create a button for the expiry checking  page
custumer_orders= tk.Button(buttons_frame, text="custumer_orders", width=15, height=2,command=Custumer_orders)
custumer_orders.pack(side="left", padx=10)
# Create a button for the update_dollor page
update_dollor = tk.Button(buttons_frame, text="update_dollor", width=15, height=2, command=update_dollor)
update_dollor.pack(side="left", padx=10)
search_order_by_no = tk.Button(buttons_frame, text="search_order_by_no", width=15, height=2, command=search_order_by_no)
search_order_by_no.pack(side="left", padx=10)

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