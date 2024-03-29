
import tkinter as tk
from tkinter import ttk
import mysql.connector
from datetime import datetime, timedelta

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
product_treeview.grid(row=0,column=0)
# Connect to the database
# set the column widths
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
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bilal@123@",
    database="testno10"
)

# Function tload the product list into the treeview object
def show():
    product_treeview.delete(*product_treeview.get_children())

    # Retrieve all products from the database
    cursor = conn.cursor()
    query = "SELECT * FROM product ORDER BY p_name ASC"
    cursor.execute(query)
    products = cursor.fetchall()

    # Define the color codes for the rows based on their expiry status
    today = datetime.today().date()
    soon = today + timedelta(days=100)
    colors = {'soon': 'red', 'normal': '', 'future': 'green'}
    # Insert each product into the treeview object, and color-code based on expiry status
    for product in products:
        expiry_date = product[6].strftime('%Y-%m-%d')
        expiry_date = datetime.strptime(expiry_date, "%Y-%m-%d").date()
        if expiry_date < today:
            color = colors['soon']
        elif expiry_date < soon:
            color = colors['future']
        else:
            color = colors['normal']
        product_treeview.insert("", "end", text=product[0], values=(product[1], product[2], product[3], product[4],
                                                                    product[5], product[6], product[7], product[8]),
                                tags=color)

    # Assign the tag configuration to the color codes
    product_treeview.tag_configure('red', background='red')
    product_treeview.tag_configure('green', background='green')
show()

# Create a frame to hold the entry widgets and labels for updating and adding products
frame = tk.Frame(root)
frame.grid(row=1,column=0)

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

# Function to retrieve selected row details and populate update entries
def update_product():
    try:
        selected_row = product_treeview.focus()
        row_details = product_treeview.item(selected_row)['values']
        p_name_entry.delete(0, tk.END)
        p_name_entry.insert(0, row_details[0])
        p_description_entry.delete(0, tk.END)
        p_description_entry.insert(0, row_details[1])
        p_cost_entry.delete(0, tk.END)
        p_cost_entry.insert(0, row_details[2])
        p_sell_price_entry.delete(0, tk.END)
        p_sell_price_entry.insert(0, row_details[3])
        p_quantity_entry.delete(0, tk.END)
        p_quantity_entry.insert(0, row_details[4])
        p_expiry_entry.delete(0, tk.END)
        p_expiry_entry.insert(0, row_details[5])
        p_company_entry.delete(0, tk.END)
        p_company_entry.insert(0, row_details[6])
        p_country_entry.delete(0, tk.END)
        p_country_entry.insert(0, row_details[7])
    except:
        print("An exception occurred")
# Function to save updated product details to the database
def save_changes():
    try:
        selected_row = product_treeview.focus()
        row_id = product_treeview.item(selected_row)['text']
        updated_name = p_name_entry.get()
        updated_description = p_description_entry.get()
        updated_cost = p_cost_entry.get()
        updated_sell_price = p_sell_price_entry.get()
        updated_quantity = p_quantity_entry.get()
        updated_expiry = p_expiry_entry.get()
        updated_company = p_company_entry.get()
        updated_country = p_country_entry.get()
        update_query = f"UPDATE product SET p_name='{updated_name}', p_description='{updated_description}', " \
                        f"p_cost={updated_cost}, p_sell_price={updated_sell_price}, p_quantity={updated_quantity}, " \
                        f"p_expiry='{updated_expiry}', p_company='{updated_company}', p_country='{updated_country}' " \
                        f"WHERE p_id={row_id}"
        cursor = conn.cursor()
        cursor.execute(update_query)
        conn.commit()
        cursor.close()
    # Refresh the treeview object to show updated information
        product_treeview.item(selected_row, values=(updated_name, updated_description, updated_cost, updated_sell_price,
                                                updated_quantity, updated_expiry, updated_company, updated_country))
    # Clear the update entries
        p_name_entry.delete(0, tk.END)
        p_description_entry.delete(0, tk.END)
        p_cost_entry.delete(0, tk.END)
        p_sell_price_entry.delete(0, tk.END)
        p_quantity_entry.delete(0, tk.END)
        p_expiry_entry.delete(0, tk.END)
        p_company_entry.delete(0, tk.END)
        p_country_entry.delete(0, tk.END)
        show()
    except:
        print("exception is ocure")

# Create Update, Add new product and Save buttons
update_button = tk.Button(frame, text="Update Product", command=update_product)
update_button.grid(row=8, column=0, pady=(10, 0))


save_button = tk.Button(frame, text="Save Changes", command=save_changes)
save_button.grid(row=8, column=2, pady=(10, 0))

# Start the tkinter event loop
root.mainloop()