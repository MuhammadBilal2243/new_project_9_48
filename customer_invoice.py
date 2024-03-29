import datetime
import subprocess
import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from fpdf import FPDF

# Create a global variable to store the database connection
conn = None

# Create a global variable to store the customer ID
c_id = None
o_id=None
# Create a global variable to store the selected items
items_list = []
# Create a global variable to store the sell prices of products
sell_price_dict = {}
# Create a global variable to store the total price
total_pkr = 0
def connect_to_database():
    global conn
    # Create a connection to the MySQL server
    conn = mysql.connector.connect(
        host="localhost",
        user="root",
        password="bilal@123@",
        database="testno10"
    )
connect_to_database()
def dollor_p():
    cursor = conn.cursor()
    sql = "SELECT rate FROM pkr WHERE id = 1"
    cursor.execute(sql)
    result = cursor.fetchone()
    conn.commit()
    cursor.close()
    print(type(result))
    return result[0]

dolor = dollor_p()
def close_database_connection():
    # Close the database connection
    if conn is not None:
        conn.close()

def insert_customer(c_name, c_phone_no, c_address, c_company, c_email, c_cnic):
    # Create a cursor to execute queries
    cursor = conn.cursor()

    # Add new customer to database
    sql = "INSERT INTO customer (c_name, c_phone_no, c_address, c_compony,c_remaining_bill ,c_email, c_cnic) VALUES (%s, %s,%s, %s, %s, %s, %s)"
    cursor.execute(sql, (c_name, c_phone_no, c_address, c_company,0, c_email, c_cnic))
    conn.commit()

    # Close the cursor
    cursor.close()

    return cursor.lastrowid

def get_customer_id(c_name, c_phone_no):
    # Create a cursor to execute queries
    cursor = conn.cursor()

    # Check if customer already exists
    sql = "SELECT c_id FROM customer WHERE c_name = %s AND c_phone_no = %s"
    cursor.execute(sql, (c_name, c_phone_no))
    result = cursor.fetchone()

    # Close the cursor
    cursor.close()

    if result:
        # Customer already exists in database
        return result[0]

    else:
        return None
def insert_order(c_id, o_date, o_time, o_amount, o_paid_amount):
    global o_id # Create a cursor to execute queries
    cursor = conn.cursor()

    # Define the SQL query to insert data into the orders table
    query = "INSERT INTO orders (c_id, o_date, o_time, o_amount, o_paid_amount) VALUES (%s, %s, %s, %s, %s)"

    # Execute the SQL query with the provided data
    cursor.execute(query, (c_id, o_date, o_time, o_amount, o_paid_amount))
    # Get the ID of the last inserted row
    o_id = cursor.lastrowid
    conn.commit()
    # Close the cursor
    remaing=0
    cursor.close()
    cursor = conn.cursor()
    query = f"select c_remaining_bill from  customer WHERE (c_id = {c_id})"
    cursor.execute(query)
    r= cursor.fetchone()
    remaing=int(r[0])
    conn.commit()
    cursor.close()
    #o_amount, o_paid_amount
    if o_amount > o_paid_amount:
        chang = float(o_amount)-float(o_paid_amount)
        r = remaing + chang
        # Close the cursor
        cursor.close()
        cursor = conn.cursor()
        query = f"UPDATE customer SET c_remaining_bill = {r} WHERE (c_id = {c_id})"
        cursor.execute(query)
        conn.commit()
        cursor.close()
    if o_amount < o_paid_amount:
        chang = float(o_paid_amount)- float(o_amount)
        r = remaing - chang
        # Close the cursor
        cursor.close()
        cursor = conn.cursor()
        query = f"UPDATE customer SET c_remaining_bill = {r} WHERE (c_id = {c_id})"
        cursor.execute(query)
        conn.commit()
        cursor.close()
def load_sell_prices():
    # Create a cursor to execute queries
    cursor = conn.cursor()

    # Get the product names and sell prices from the database
    cursor.execute("SELECT p_id, p_name, p_sell_price, p_quantity FROM product ORDER BY p_name ASC")
    results = cursor.fetchall()

    # Close the cursor
    cursor.close()

    return {f"{result[1]}-AVL Quantity ={result[3]} price in PKR{result[2]*dolor}": result[2] for result in results}
def submit_customer():
    global c_id

    # Get the data from the inputs
    c_name = name_entry.get()
    c_phone_no = phone_no_entry.get()
    c_address = address_entry.get()
    c_company = company_entry.get()
    c_email = email_entry.get()

    c_cnic = cnic_entry.get()
    # Check if customer already exists
    c_id = get_customer_id(c_name, c_phone_no)
    if c_id is None:
        # Add new customer to database
        c_id = insert_customer(c_name, c_phone_no, c_address, c_company, c_email, c_cnic)
    # Update the c_id label
    c_id_label.config(text=f"Customer ID: {c_id}")
def clear_inputs():
    # Clear the input fields
    global total_pkr, items_list
    total_pkr=[]
    items_list=[]
    name_entry.delete(0, tk.END)
    phone_no_entry.delete(0, tk.END)
    address_entry.delete(0, tk.END)
    company_entry.delete(0, tk.END)
    email_entry.delete(0, tk.END)
    cnic_entry.delete(0, tk.END)
    tree.delete(*tree.get_children())
    # Clear the c_id label
    c_id_label.config(text="")
    global c_id
    c_id = None
def add_item():
    global total_pkr, items_list

    # Get the selected product, sell price and quantity
    product_name,qy = product_picker.get().split("-")
    sell_price = sell_price_dict[product_picker.get()]*dolor
    quantity = int(quantity_picker.get())

    # Get the product id from the database
    cursor = conn.cursor()
    cursor.execute("SELECT p_id ,p_quantity FROM product WHERE p_name = %s", (product_name,))
    result = cursor.fetchone()
    cursor.close()
    print(result)
    if result[1] >= quantity:
        p_id = result[0]
    else:
        messagebox.showerror("Error", "quantity is less in store")
        return

    # Check if the product already exists in the items_list
    for i, item in enumerate(items_list):
        if item[0] == product_name:
            if result[1] >= item[3] + quantity:
                p_id = result[0]
                items_list[i] = (product_name, p_id, sell_price, item[3] + quantity, sell_price * (item[3] + quantity))
                break
            else:
                messagebox.showerror("Error", "quantity is less in store")
                return
                break
            # Product already exists, update the quantity and price_total_pkr

    else:
        # Product does not exist, add it to the items_list
        price_total_pkr = sell_price * quantity
        items_list.append((product_name, p_id, sell_price, quantity, price_total_pkr))

    # Clear the previous items from the treeview
    tree.delete(*tree.get_children())

    # Add the new items to the treeview and calculate the total
    total_pkr = 0
    for item in items_list:
        tree.insert("", tk.END, values=(item[0], item[1], item[2], item[3], item[4]))
        total_pkr += item[4]
    total_label.config(text=f"Total: PKR {total_pkr}")
def remove_item():
    global total_pkr, items_list
    # Get the selected item from the treeview
    selected_item = tree.selection()

    if selected_item:
        # Remove the selected item from the items_list
        item_index = tree.index(selected_item)
        item = items_list[item_index]
        items_list.remove(item)

        # Clear the previous items from the treeview
        tree.delete(selected_item)

        # Add the new items to the treeview and calculate the total
        total_pkr = 0
        for item in items_list:
            tree.insert("", tk.END, values=(item[0], item[1], item[2], item[3], item[4]))

            # Add the item price to the total price
            total_pkr += item[4]

        # Update the total price label
        total_label.config(text=f"Total: PKR {total_pkr}")
# Define the function to download the invoice as PDF
def download_pdf(x):
    # Retrieve the order number entered by the user
    order_no = x

    # Create the invoice PDF
    pdf = FPDF()
    # Add a page
    pdf.add_page()

    # Retrieve the invoice details from the database
    cursor = conn.cursor()
    query = f"SELECT o.c_id, c.c_name, c.c_phone_no, c.c_address, c.c_compony, c.c_email, c.c_cnic, " \
            f"o.o_date, o.o_time, o.o_amount, o.o_paid_amount " \
            f"FROM Orders o " \
            f"INNER JOIN customer c ON c.c_id = o.c_id " \
            f"WHERE o.o_id = {order_no};"
    cursor.execute(query)
    invoice_detail = cursor.fetchone()

    # Retrieve all products with their quantity and sell price
    query = f"SELECT p.p_name, oi.order_quantity, oi.product_price_pkr " \
            f"FROM order_items oi " \
            f"INNER JOIN product p ON p.p_id = oi.p_id " \
            f"WHERE oi.o_id = {order_no};"
    cursor.execute(query)
    product_detail = cursor.fetchall()
    #heading of company
    pdf.set_font('Arial', 'B', 16)
    pdf.cell(0, 10, f"smart motion company", 0, 1)
    # Add the invoice details to the PDF
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(0, 10, f"Invoice {order_no}", 0, 1)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, "Invoice Date:", 1)
    pdf.cell(40, 10, str(invoice_detail[7]), 1)
    pdf.cell(40, 10, "Invoice Time:", 1)
    pdf.cell(40, 10, str(invoice_detail[8]), 1)
    pdf.cell(0, 10, "", 0, 1)
    pdf.cell(40, 10, "Invoice Amount:", 1)
    pdf.cell(40, 10, str(invoice_detail[9]), 1)
    pdf.cell(40, 10, "Paid Amount:", 1)
    pdf.cell(40, 10, str(invoice_detail[10]), 1)
    pdf.cell(0, 10, "", 0, 1)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, "Customer Name:", 1)
    pdf.cell(100, 10, str(invoice_detail[1]), 1)
    pdf.cell(0, 10, "", 0, 1)
    pdf.cell(40, 10, "C_Phone_No:", 1)
    pdf.cell(60, 10, str(invoice_detail[2]), 1)
    pdf.cell(40, 10, "Customer CNIC:", 1)
    pdf.cell(50, 10, str(invoice_detail[6]), 1)
    pdf.cell(0, 10, "", 0, 1)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(40, 10, "Customer Address:", 1)
    pdf.cell(0, 10, str(invoice_detail[3]), 1)
    pdf.cell(0, 10, "", 0, 1)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(45, 10, "Customer Company:", 1)
    pdf.cell(100, 10, str(invoice_detail[4]), 1)
    pdf.cell(0, 10, "", 0, 1)
    pdf.cell(45, 10, "Customer Email:", 1)
    pdf.cell(0, 10, str(invoice_detail[5]), 1)
    pdf.cell(0, 10, "", 0, 1)
    pdf.set_font('Arial', 'B', 12)
    pdf.cell(20, 10, "ID", 1)
    pdf.cell(80, 10, "Product Name", 1)
    pdf.cell(30, 10, "Product Price", 1)
    pdf.cell(30, 10, "Quantity", 1)
    pdf.cell(30, 10, "Total Price", 1)
    pdf.cell(0, 10, "", 0, 1)

    # Add the product details to the PDF
    pdf.set_font('Arial', '', 12)
    for idx, (product_name, order_quantity, product_price) in enumerate(product_detail):
        total_price = round( product_price, 2)
        pdf.cell(20, 10, str(idx+1), 1)
        pdf.cell(80, 10, product_name, 1)
        pdf.cell(30, 10, str(product_price/order_quantity), 1)
        pdf.cell(30, 10, str(order_quantity), 1)
        pdf.cell(30, 10, str(total_price), 1)
        pdf.cell(0, 10, "", 0, 1)
    # Close the PDF
    pdf.output(f"Invoice no-{order_no}.pdf")

    # Close the cursor
    cursor.close()
def print_invoice():
    global c_id, total_pkr, items_list, o_id

    try:
        # Get the number from the Entry widget
        paid_amount = float(paid_entry.get())
    except ValueError:
        # Handle the case when the input is not a number
        messagebox.showerror("Error", "Invalid input. Please try again.")
        return

    # Get the current date and time
    current_date = datetime.date.today()
    current_time = datetime.datetime.now().time()

    if c_id is None:
        messagebox.showerror("Error", "Please select a customer first.")
        return

    insert_order(c_id, current_date, current_time, total_pkr, paid_amount)

    # Open a new window to show the invoice data
    invoice_window = tk.Toplevel(window)
    invoice_window.title("Invoice")

    # Create a label to display the customer details
    customer_O_id_label = tk.Label(invoice_window, text=f"Oreder no : {o_id}")
    customer_O_id_label.pack()
    customer_name_label = tk.Label(invoice_window, text=f"Name: {name_entry.get()}")
    customer_name_label.pack()
    customer_phone_label = tk.Label(invoice_window, text=f"Phone: {phone_no_entry.get()}")
    customer_phone_label.pack()
    customer_address_label = tk.Label(invoice_window, text=f"Address: {address_entry.get()}")
    customer_address_label.pack()
    # Create a treeview to display the order items
    item_tree = ttk.Treeview(invoice_window, columns=["Product", "Quantity", "Price (PKR)"])
    item_tree.column("#0", width=0, stretch=tk.NO)
    item_tree.column("Product", anchor=tk.W, width=200)
    item_tree.heading("Product", text="Product", anchor=tk.W)
    item_tree.column("Quantity", anchor=tk.CENTER, width=100)
    item_tree.heading("Quantity", text="Quantity", anchor=tk.CENTER)
    item_tree.column("Price (PKR)", anchor=tk.CENTER, width=120)
    item_tree.heading("Price (PKR)", text="Price (PKR)", anchor=tk.CENTER)
    item_tree.pack()
    # Insert the order items into the treeview
    for product in items_list:
        quantity = product[3]
        price_pkr = product[4]
        item_tree.insert("", tk.END, values=(product[0], quantity, price_pkr))
        cursor = conn.cursor()
        # Define the data to be inserted into the order_items table
        p_idd = product[1]
        order_quantity = quantity
        product_price_pkr = product[4]
        # Define the SQL query to insert data into the order_items table
        query = "INSERT INTO order_items (p_id, o_id, order_quantity, product_price_pkr) VALUES (%s, %s, %s, %s)"
        # Execute the SQL query with the provided data
        cursor.execute(query, (p_idd, o_id, order_quantity, product_price_pkr))
        # Commit the changes to the database
        conn.commit()
        # Close the cursor and connection
        cursor.close()
        p_idd,order_quantity
        # Close the cursor
        cursor.close()
        cursor = conn.cursor()
        query = f"select p_quantity from product WHERE (p_id = {p_idd})"
        cursor.execute(query)
        q = cursor.fetchone()
        cursor.close()
        up=int(q[0])-order_quantity
        cursor = conn.cursor()
        query = f"UPDATE product SET p_quantity = {up} WHERE (p_id = {p_idd})"
        cursor.execute(query)
        conn.commit()
        cursor.close()

    # Create a label to display the total price
    total_price_label = tk.Label(invoice_window, text=f"Total: PKR {total_pkr}")
    total_price_label.pack()

    # Create a label to display the paid amount
    paid_amount_label = tk.Label(invoice_window, text=f"Paid: PKR {paid_amount}")
    paid_amount_label.pack()
    # Create a label to display the remaining amount
    remaining_amount = float(total_pkr) - paid_amount
    remaining_amount_label = tk.Label(invoice_window, text=f"Remaining: PKR {remaining_amount}")
    remaining_amount_label.pack()
    download_pdf(o_id)
def update_sell_price(event):
    product_name = product_picker.get()
    if product_name in sell_price_dict:
        sell_price_label.config(text=f"dolor {sell_price_dict[product_name]} x PKR {dolor}")
    else:
        sell_price_label.config(text="")
# Create a tkinter window
bgcolor="#FFFFFF"
bgcolor1='#FFFFFF'
window = tk.Tk()
window.configure(bg=bgcolor)
window.title("Customer Entry",)

# Connect to the database
connect_to_database()
# Create the customer frame to group the input fields
def home():
    subprocess.Popen(["python", "home.py"])
    window.destroy()
header_frame = tk.Frame(window, padx=10, pady=10, bg=bgcolor)
header_frame.pack()
home_buttun = tk.Button(header_frame,text="back to Home ", padx=10, pady=10, bg=bgcolor,command=home)
home_buttun.grid(row=0, column=0 )

tk.Label(header_frame, text="this my shop name heading :",font=("Arial", 20, "bold")).grid(row=0, column=2,padx=203)

# Create the customer frame to group the input fields
customer_frame = tk.Frame(window, padx=10, pady=10, bg=bgcolor)
customer_frame.pack()

tk.Label(customer_frame, text="Name:",bg=bgcolor1).grid(row=0, column=0)
name_entry = tk.Entry(customer_frame,bg=bgcolor1)
name_entry.grid(row=0, column=1)

tk.Label(customer_frame, text="Phone Number:",bg=bgcolor1).grid(row=1, column=0)
phone_no_entry = tk.Entry(customer_frame,bg=bgcolor1)
phone_no_entry.grid(row=1, column=1)

tk.Label(customer_frame, text="Address:",bg=bgcolor1).grid(row=2, column=0)
address_entry = tk.Entry(customer_frame,bg=bgcolor1)
address_entry.grid(row=2, column=1)

tk.Label(customer_frame, text="Company Name:",bg=bgcolor1).grid(row=3, column=0)
company_entry = tk.Entry(customer_frame,bg=bgcolor1)
company_entry.grid(row=3, column=1)

tk.Label(customer_frame, text="Email Address:",bg=bgcolor1).grid(row=4, column=0)
email_entry = tk.Entry(customer_frame,bg=bgcolor1)
email_entry.grid(row=4, column=1)

tk.Label(customer_frame, text="CNIC Number:",bg=bgcolor1).grid(row=6, column=0)
cnic_entry = tk.Entry(customer_frame,bg=bgcolor1)
cnic_entry.grid(row=6, column=1)

# Create a Submit button to insert the customer
submit_btn = tk.Button(customer_frame, text="Submit",bg=bgcolor, command=submit_customer)
submit_btn.grid(row=7, column=0)

# Create a Clear button to clear the inputs
clear_btn = tk.Button(customer_frame, text="Clear",bg=bgcolor, command=clear_inputs)
clear_btn.grid(row=7, column=1)

# Create a label to display the c_id of the newly created customer
c_id_label = tk.Label(window, text="",bg=bgcolor)
c_id_label.pack()

# Load the product sell prices from the database
sell_price_dict = load_sell_prices()

# Create the invoice entries frame
invoice_entries_frame = tk.Frame(window, padx=10, pady=10, relief=tk.RAISED, bd=1,bg=bgcolor)
invoice_entries_frame.pack()

# Create the product picker combo box
tk.Label(customer_frame, text="Product:",bg=bgcolor1).grid(row=0, column=2)
product_picker = ttk.Combobox(customer_frame, values=list(sell_price_dict.keys()), width=50)
product_picker.grid(row=0, column=3)

# Create the sell price label
tk.Label(customer_frame, text="dolor rate:",bg=bgcolor1).grid(row=1, column=2)
sell_price_label = tk.Label(customer_frame,bg=bgcolor1, text="")
sell_price_label.grid(row=1, column=3)

# Create the quantity combo box
tk.Label(customer_frame, text="Quantity:",bg=bgcolor1).grid(row=0, column=4)
quantity_picker = ttk.Combobox(customer_frame, values=[1, 2, 3, 4, 5])
quantity_picker.grid(row=0, column=5)

# Create the add button
add_btn = tk.Button(customer_frame, text="Add",bg=bgcolor, command=add_item)
add_btn.grid(row=7, column=4)

# Create the remove button
remove_btn = tk.Button(customer_frame,bg=bgcolor, text="Remove", command=remove_item)
remove_btn.grid(row=7, column=5)

#
#Create the items treeview (product_name, p_id, sell_price, quantity, price_total_pkr)
tree = ttk.Treeview(invoice_entries_frame, columns=["Product","p_id","sell_price", "Quantity", "Price (PKR)"])
tree.column("#0", width=0, stretch=tk.NO,)
tree.column("Product", anchor=tk.W, width=200)
tree.heading("Product", text="Product", anchor=tk.W)
tree.column("p_id", anchor=tk.W, width=200)
tree.heading("p_id", text="p_id", anchor=tk.W)
tree.column("sell_price", anchor=tk.W, width=200)
tree.heading("sell_price", text="sell_price", anchor=tk.W)
tree.column("Quantity", anchor=tk.CENTER, width=100)
tree.heading("Quantity", text="Quantity", anchor=tk.CENTER)
tree.column("Price (PKR)", anchor=tk.CENTER, width=120)
tree.heading("Price (PKR)", text="Price (PKR)", anchor=tk.CENTER)
tree.grid(row=2, column=0, columnspan=4, pady=10)

# Create the total label
total_label = tk.Label(invoice_entries_frame, text="Total: PKR 0")
total_label.grid(row=3, column=0)

# Create the input field for the paid amount
tk.Label(invoice_entries_frame, text="Paid Amount:").grid(row=3, column=1)
paid_entry = tk.Entry(invoice_entries_frame)
paid_entry.grid(row=3, column=2)

# Create the print button
print_btn = tk.Button(invoice_entries_frame, text="Print Invoice", command=print_invoice)
print_btn.grid(row=3, column=3)

# Update the sell price label when a product is selected
product_picker.bind("<<ComboboxSelected>>", update_sell_price)

# Start the tkinter main loop
window.mainloop()

# Close the database connection
close_database_connection()