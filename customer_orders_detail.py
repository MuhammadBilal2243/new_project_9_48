import tkinter as tk
import tkinter.ttk as ttk
import mysql.connector

# Create a connection to the MySQL server
conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bilal123",
    database="testno10"
)
# Create the tkinter window
root = tk.Tk()
root.title("Customer Orders")

# Set the style for the window and widgets
style = ttk.Style()
style.theme_use("clam")
style.configure("Treeview", background="#D3D3D3", foreground="black", rowheight=36, fieldbackground="#D3D3D3")
style.configure("TButton", background="#0078D7", foreground="white", font=("Arial", 12))
style.configure("TLabel", background="#D3D3D3", foreground="black", font=("Arial", 12))
# Create the ComboBox to display customer names and phone numbers
frame1 = tk.Frame(root)
frame1.grid(row=0, column=0, pady=10)

customer_label = ttk.Label(frame1, text="Select Customer:")
customer_label.grid(row=0, column=0, padx=10)
customer_picker = ttk.Combobox(frame1, state="readonly", width=30)
customer_picker.grid(row=0, column=1)
# Retrieve the customer names and phone numbers from the database
cursor = conn.cursor()
query = "SELECT c_name, c_phone_no FROM customer"
cursor.execute(query)
customers = cursor.fetchall()
# Add the customer names and phone numbers to the ComboBox
customer_data = [(name, phone) for name, phone in customers]
customer_picker["values"] = [f"{name}-{phone}" for name, phone in customer_data]
customer_picker.current(0)
# Create the Treeview to display orders
# Create the Treeview to display orders
order_tree = ttk.Treeview(root, columns=("id", "date", "time", "amount", "paid_amount", "remaining"), show="headings")
order_tree.heading("id", text="O_ID")
order_tree.heading("date", text="Date")
order_tree.heading("time", text="Time")
order_tree.heading("amount", text="Amount")
order_tree.heading("paid_amount", text="Paid Amount")
order_tree.heading("remaining", text="Remaining")
order_tree.grid(row=1, column=0, padx=10, pady=10)
# Function to retrieve and display orders for a selected customer
def show_orders(event):
    # Get the selected customer
    selected_customer = customer_picker.get()
    selected_customer_name, selected_customer_phone = selected_customer.split("-")
    cursor.execute(
        f"SELECT c_id  FROM customer WHERE c_name = '{selected_customer_name}' AND c_phone_no = '{selected_customer_phone}'")
    rt = cursor.fetchone()

    # Retrieve the orders for the selected customer from the database
    query = f"SELECT o_id, o_date, o_time,o_amount, o_paid_amount FROM Orders  WHERE c_id = {rt[0]}"
    cursor.execute(query)
    orders = cursor.fetchall()
    # Clear the existing orders in the Treeview
    order_tree.delete(*order_tree.get_children())

    # Add the orders for the selected customer to the Treeview
    for order in orders:
        # Calculate the remaining amount for this order
        remaining = order[3] - order[4]
        values = (*order, remaining)
        order_tree.insert("", "end", text="", values=values)
# Bind the ComboBox to the function that retrieves and displays orders
customer_picker.bind("<<ComboboxSelected>>", show_orders)

# Create a vertical scrollbar for the Treeview
scrollbar = ttk.Scrollbar(root, orient="vertical", command=order_tree.yview)
scrollbar.grid(row=1, column=1, sticky="NS")
order_tree.configure(yscrollcommand=scrollbar.set)

# Start the tkinter event loop
root.mainloop()

# Close the database connection
cursor.close()
conn.close()