import tkinter as tk
from tkinter import ttk, messagebox
import mysql.connector
from fpdf import FPDF
import fitz  # for PDF to image conversion
# Create the main window
window = tk.Tk()
window.title("Generate Invoice")
# Create a frame to hold the invoice detail
frame = ttk.Frame(window, padding="20")
frame.grid(row=0, column=0)
# Create the label and entry box for entering the order number
order_label = ttk.Label(frame, text="Enter Order Number:")
order_label.grid(row=0, column=0)
order_entry = ttk.Entry(frame)
order_entry.grid(row=0, column=1)
# Create the button to download invoice as PDF
pdf_button = ttk.Button(frame, text="Download Invoice as PDF")
pdf_button.grid(row=0, column=2)
# Define the function to download the invoice as PDF
def download_pdf():
    # Retrieve the order number entered by the user
    try:
        order_no = order_entry.get()

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
        # heading of company
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
            total_price = round(product_price, 2)
            pdf.cell(20, 10, str(idx + 1), 1)
            pdf.cell(80, 10, product_name, 1)
            pdf.cell(30, 10, str(product_price / order_quantity), 1)
            pdf.cell(30, 10, str(order_quantity), 1)
            pdf.cell(30, 10, str(total_price), 1)
            pdf.cell(0, 10, "", 0, 1)
        # Close the PDF
        pdf.output(f"Invoice-{order_no}.pdf")

        # Close the cursor
        cursor.close()
        pdf_to_pic(order_no)
        messagebox.showinfo("download successful","your order no pdf and pic is downloaded to your persnal computer")
    except:
        messagebox.showwarning("error", "we dont have this order Number in our data base.please input correct order no")

pdf_button.config(command=download_pdf)
def pdf_to_pic(order_no):
    # Bind the button to download the invoice as PDF
    # Convert the PDF to images
    pdf_file = fitz.open(f"Invoice-{order_no}.pdf")
    for page_idx in range(pdf_file.page_count):
        page = pdf_file[page_idx]
        image = page.get_pixmap()
        image.save(f"Invoice-{order_no}_page{page_idx + 1}.png")

    # Display the images in a new window
    pdf_window = tk.Toplevel(window)
    pdf_window.title(f"Invoice {order_no}")
    pdf_window.geometry("800x800")

    # Load the images into labels and display in a grid layout
    for page_idx in range(pdf_file.page_count):
        image = tk.PhotoImage(file=f"Invoice-{order_no}_page{page_idx + 1}.png")
        label = ttk.Label(pdf_window, image=image)
        label.image = image
        label.grid(row=page_idx // 2, column=page_idx % 2)

    # Close the PDF file
    pdf_file.close()
# Start the main event loop


conn = mysql.connector.connect(
    host="localhost",
    user="root",
    password="bilal@123@",
    database="testno10"
)
window.mainloop()

# Close the database connection
conn.close()
