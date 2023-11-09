
import tkinter as tk
from tkinter import ttk
import mysql.connector

# Create a tkinter window
root = tk.Tk()
root.title("Product List")

# Create a treeview object to display the product list
product_treeview = ttk.Treeview(root, columns=("p_name", "p_description", "p_cost",
                                                "p_sell_price", "p_quantity", "p_expiry", "p_company", "p_country"))
product_treeview.heading("#0", text="ID")
product_treeview.heading("p_name", text="Product Name")
product_treeview.heading("p_description", text="Description")
product_treeview.heading("p_cost", text="Cost ($)")
product_treeview.heading("p_sell_price", text="Selling Price ($)")
product_treeview.heading("p_quantity", text="Quantity")
product_treeview.heading("p_expiry", text="Expiry")
product_treeview.heading("p_company", text="Company")
product_treeview.heading("p_country", text="Country")
product_treeview.column("#0", width=50)
product_treeview.column("p_name", width=150)
product_treeview.column("p_description", width=200)
product_treeview.column("p_cost", width=100)
product_treeview.column("p_sell_price", width=150)
product_treeview.column("p_quantity", width=100)
product_treeview.column("p_expiry", width=100)
product_treeview.column("p_company", width=150)
product_treeview.column("p_country", width=100)

product_treeview.grid(row=0, column=0)

product_treeview.pack()

# Connect to the database
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bilal123",
    database="testno10"
)

# Function to load the product list into the treeview object
def show():
    cursor = conn.cursor()
    query = "SELECT * FROM product ORDER BY p_name ASC"
    cursor.execute(query)
    products = cursor.fetchall()
    for product in products:
        product_treeview.insert("", "end", text=product[0], values=(product[1], product[2], product[3], product[4],
                                                                 product[5], product[6], product[7], product[8]))
    cursor.close()

show()

# Create a frame to hold the entry widgets and labels for updating and adding products
frame = tk.Frame(root)
frame.pack(fill='x')

# Create labels and entry widgets for updating product details
p_name_label = tk.Label(frame, text="Product Name:")
p_name_label.grid(row=0, column=0)

p_description_label = tk.Label(frame, text="Description:")
p_description_label.grid(row=1, column=0)

p_cost_label = tk.Label(frame, text="Cost (PKR):")
p_cost_label.grid(row=2, column=0)

p_sell_price_label = tk.Label(frame, text="Selling Price (PKR):")
p_sell_price_label.grid(row=3, column=0)

p_quantity_label = tk.Label(frame, text="Quantity:")
p_quantity_label.grid(row=4, column=0)

p_expiry_label = tk.Label(frame, text="Expiry Date:YYYY-MM-DD")
p_expiry_label.grid(row=5, column=0)

p_company_label = tk.Label(frame, text="Company:")
p_company_label.grid(row=6, column=0)

p_country_label = tk.Label(frame, text="Country:")
p_country_label.grid(row=7, column=0)

p_name_entry = tk.Entry(frame, width=30)
p_name_entry.grid(row=0, column=1)

p_description_entry = tk.Entry(frame, width=30)
p_description_entry.grid(row=1, column=1)

p_cost_entry = tk.Entry(frame, width=30)
p_cost_entry.grid(row=2, column=1)

p_sell_price_entry = tk.Entry(frame, width=30)
p_sell_price_entry.grid(row=3, column=1)

p_quantity_entry = tk.Entry(frame, width=30)
p_quantity_entry.grid(row=4, column=1)

p_expiry_entry = tk.Entry(frame, width=30)
p_expiry_entry.grid(row=5, column=1)

p_company_entry = tk.Entry(frame, width=30)
p_company_entry.grid(row=6, column=1)

p_country_entry = tk.Entry(frame, width=30)
p_country_entry.grid(row=7, column=1)

# Function to add new products to the database
def add_product():
    try:
        name = p_name_entry.get()
        description = p_description_entry.get()
        cost = p_cost_entry.get()
        sell_price = p_sell_price_entry.get()
        quantity = p_quantity_entry.get()
        expiry = p_expiry_entry.get()
        company = p_company_entry.get()
        country = p_country_entry.get()
        insert_query = f"INSERT INTO product (p_name, p_description, p_cost, p_sell_price, p_quantity, p_expiry, " \
                   f"p_company, p_country) VALUES ('{name}', '{description}', {cost}, {sell_price}, {quantity}, " \
                   f"'{expiry}', '{company}', '{country}')"
        cursor = conn.cursor()
        cursor.execute(insert_query)
        conn.commit()
        cursor.close()

    # Refresh the treeview object to show updated information
        product_treeview.delete(*product_treeview.get_children())
        show()

        # Clear the add new product entries
        p_name_entry.delete(0, tk.END)
        p_description_entry.delete(0, tk.END)
        p_cost_entry.delete(0, tk.END)
        p_sell_price_entry.delete(0, tk.END)
        p_quantity_entry.delete(0, tk.END)
        p_expiry_entry.delete(0, tk.END)
        p_company_entry.delete(0, tk.END)
        p_country_entry.delete(0, tk.END)
        # set the column widths
    except:
        print("put product detail  corectly")


add_button = tk.Button(frame, text="Add New Product", command=add_product)
add_button.grid(row=8, column=1, pady=(10,0))
# Start the tkinter event loop
root.mainloop()