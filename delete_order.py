
from tkinter import *
import mysql.connector


# Function to connect to the database
def connect_to_db():
    try:
        # Update the database details according to your setup
        conn = mysql.connector.connect(

            host = "localhost",
            user = "root",
            password = "bilal123",
            database = "testno10"
        )
        return conn
    except mysql.connector.Error as err:
        print("Error connecting to the database: ", err)
        return None


# Function to delete order from database
def delete_order():
    # Get the order ID from the entry field
    order_id = int(entry_order_id.get())

    # Connect to the database
    conn = connect_to_db()
    if not conn:
        return

    try:
        # Create a cursor to execute SQL queries
        cursor = conn.cursor()

        # Delete the order from the order_items table
        query = "DELETE FROM order_items WHERE o_id = %s"
        cursor.execute(query, (order_id,))

        # Delete the order from the Orders table
        query = "DELETE FROM Orders WHERE o_id = %s"
        cursor.execute(query, (order_id,))

        # Commit the changes to the database
        conn.commit()

        # Close the cursor and connection
        cursor.close()
        conn.close()

        # Reset the entry field
        entry_order_id.delete(0, END)
        # Show a success message
        label_result.config(text="Order deleted successfully.")
    except mysql.connector.Error as err:
        print("Error deleting order from database: ", err)
        label_result.config(text="Error deleting order from database.")

# Create the tkinter window
window = Tk()

# Set the window title
window.title("Delete Order by number ")

# Create labels and entry fields
label_order_id = Label(window, text="Order ID:")
label_order_id.grid(row=0, column=0, padx=10, pady=10)
entry_order_id = Entry(window)
entry_order_id.grid(row=0, column=1, padx=10, pady=10)

# Create a button to delete the order
button_delete = Button(window, text="Delete Order", command=delete_order)
button_delete.grid(row=1, column=0, columnspan=2, padx=10, pady=10)

# Create a label to display the result
label_result = Label(window, text="")
label_result.grid(row=2, column=0, columnspan=2, padx=10, pady=10)

# Start the tkinter event loop
window.mainloop()