import os
import streamlit as st
import mysql.connector
import random
from datetime import datetime


# Retrieve user_id from environment variable
user_id = os.environ.get("USER_ID")  # Change this to USER_ID

# Connect to the database and fetch customer information
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="dbms_project"
)
cursor = db.cursor()
query_customer = f"SELECT * FROM Customer WHERE CustomerID = '{user_id}'"
cursor.execute(query_customer)
customer_info = cursor.fetchone()

# Define custom CSS styles
custom_css = """
<style>
.burger-menu {
    font-size: 20px;
}

.sidebar-content {
    margin-left: 20px;
}
</style>
"""

# Apply custom CSS
st.markdown(custom_css, unsafe_allow_html=True)

# Sidebar navigation with burger menu
st.sidebar.markdown('<p class="burger-menu">&#x2630; Navigation</p>', unsafe_allow_html=True)
selected_tab = st.sidebar.radio("", ["Products", "Purchase History", "Shopping Cart", "Customer Profile", "Transaction History","Update Information"], key='1')

# Display content based on selected tab
if selected_tab == "Products":
    # Code for displaying products
    st.title('Products')
    # Fetch all rows from the Products table
    query_products = "SELECT * FROM Product"
    cursor.execute(query_products)
    products = cursor.fetchall()

    # Display products in a single column
    # col1, _ = st.columns(2)

    for product in products:
        # Create a unique key for each button using the product ID
        button_key = f"add_to_cart_{product[0]}"

        # Calculate discounted price
        discounted_price = product[3] * (1 - product[7] / 100)  # Assuming discount is stored as an integer (e.g., 10 for 10%)
  # Assuming discount is stored as a decimal (e.g., 0.1 for 10%)

        # Display product details in a card format
        # Set the width of the column to expand it
        col1, _ = st.columns([10, 1])  # You can adjust the width ratios as needed

        # Display product details in a card format
        col1.text(f"Product ID: {product[0]}")
        col1.text(f"Name: {product[1]}")
        col1.text(f"Price: {product[3]:.2f}")
        col1.text(f"Discount: {product[7]}%")
        col1.text(f"Discounted Price: {discounted_price:.2f}")
        col1.text(f"Stock: {product[4]}")
        col1.text(f"Description: {product[6]}")

        add_to_cart = col1.button("Add to Cart", key=button_key)


        if add_to_cart:
            # Logic to add product to shopping cart using session data
            shopping_cart = st.session_state.get("shopping_cart", [])
            shopping_cart.append({
                "product_id": product[0],
                "name": product[1],
                "price": discounted_price,  # Use the discounted price
                "quantity": 1,  # You can set the initial quantity
            })
            st.session_state.shopping_cart = shopping_cart
            st.success("Product added to the shopping cart!")

# ... (remaining code)


elif selected_tab == "Transaction History":
    # Display Transaction history details
    st.title("Transaction History")

    if customer_info:
        # Fetch and display Transaction for the specific user
        query_transaction_history = f"""
            SELECT t.TransactionID, t.DateAndTime, t.TotalAmount, t.PaymentMethod, e.Name AS EmployeeName, c.Address
            FROM Transaction t
            JOIN Employee e ON t.EmployeeID = e.EmployeeID
            JOIN Customer c ON t.CustomerID = c.CustomerID
            WHERE t.CustomerID = '{user_id}'
        """
        cursor.execute(query_transaction_history)
        transaction_history = cursor.fetchall()

        if transaction_history:
            # Create a DataFrame for the transaction history
            import pandas as pd
            columns = ["Transaction ID", "Date and Time", "Total Amount", "Payment Method", "Employee Name", "Customer Address"]
            df = pd.DataFrame(transaction_history, columns=columns)

            # Display the transaction history table
            st.table(df)
        else:
            st.write("No transaction history found for this customer.")
    else:
        st.error("Customer not found in the database. Please check the ID.")
# ... (previous code)

elif selected_tab == "Customer Profile":
    # Display customer information
    st.title("Customer Profile")
    if customer_info:
        st.markdown(f"**Customer ID:** {customer_info[0]}")
        st.markdown(f"**Name:** {customer_info[1]}")
        st.markdown(f"**Contact Information:** {customer_info[2]}")
        st.markdown(f"**Address:** {customer_info[3]}")
        st.markdown(f"**Loyalty Points:** {customer_info[4]}")

        delete_customer_button = st.button("Delete Customer", key="delete_customer_button")
        if delete_customer_button:
            # Delete customer from the database
            customer_info = []
            query_delete_customer = f"DELETE FROM Customer WHERE CustomerID = '{user_id}'"
            cursor.execute(query_delete_customer)
            db.commit()
            st.success("Customer deleted successfully!")
            # Clear the customer_info after successful deletion
            customer_info = None
    else:
        st.error("Customer not found in the database. Please check the ID.")

elif selected_tab=="Update Information":
    st.title('Update Information')
    field_to_update = st.selectbox("Select Field to Update", ["Name", "ContactInformation", "Address"])
    new_value = st.text_input(f"Enter New {field_to_update}:")

    pay_now = st.button(f"Update {field_to_update}")
    if pay_now:
        query_update_customer = f"UPDATE Customer SET {field_to_update} = '{new_value}' WHERE CustomerID = '{user_id}'"
        cursor.execute(query_update_customer)
        db.commit()
        st.success(f"Customer {field_to_update} updated successfully!")
        # Update displayed customer_info
        customer_info = (user_id, customer_info[1], customer_info[2], customer_info[3], customer_info[4], customer_info[5])
# ... (previous code)

# Code for displaying shopping cart
elif selected_tab == "Shopping Cart":
    st.title("Shopping Cart")

    # Retrieve shopping cart from session data
    shopping_cart = st.session_state.get("shopping_cart", [])

    total_amount = 0

    for cart_item in shopping_cart:
        st.text(f"Product ID: {cart_item['product_id']}\nName: {cart_item['name']}\nPrice: {cart_item['price']}\nQuantity: {cart_item['quantity']}")

        # Add validation to check if the price can be converted to a float
        try:
            price = float(cart_item['price'])
        except ValueError:
            st.warning(f"Invalid price for product ID {cart_item['product_id']}: {cart_item['price']}")
            continue

        # Add validation to check if the quantity can be converted to an integer
        try:
            quantity = int(cart_item['quantity'])
        except ValueError:
            st.warning(f"Invalid quantity for product ID {cart_item['product_id']}: {cart_item['quantity']}")
            continue

        total_amount += price * quantity

    st.markdown(f"**Total Amount:** {total_amount}")

    payment_method = st.radio(
        "Select Payment Method",
        ["Cash", "Credit Card", "Debit Card", "UPI"]
    )

    pay_now = st.button(f"Pay Using {payment_method}")

    if pay_now:
        # Generate random TransactionID
        tID = random.randint(1000, 99999)

        # Get current date and time
        time = datetime.now()

        # Set CustomerID (You may need to modify this based on your application)
        customerId = user_id

        # Select EmployeeID from 'finance' department
        query_employee = "SELECT EmployeeID FROM employee WHERE Department = 'sales' ORDER BY RAND() LIMIT 1"
        cursor.execute(query_employee)
        employee_result = cursor.fetchone()
        employeeId = employee_result[0] if employee_result else None

        # Insert into transaction table
        query_transaction = f"""
            INSERT INTO Transaction (TransactionID, DateAndTime, CustomerID, EmployeeID, TotalAmount, PaymentMethod)
            VALUES ('{tID}', '{time}', '{customerId}', '{employeeId}', {total_amount}, '{payment_method}')
        """
        cursor.execute(query_transaction)
        db.commit()  # Commit the transaction to the database

        # Insert into purchases table
        for cart_item in shopping_cart:
            product_id = cart_item['product_id']
            quantity_bought = cart_item['quantity']

            # Insert into purchases table
            query_add_purchase = f"""
        INSERT INTO purchase_history (customerid, ProductID, QuantityBought, PurchaseDate)
        VALUES ('{customerId}', '{product_id}', {quantity_bought}, NOW())
    """

            cursor.execute(query_add_purchase)
            db.commit()

            # Update QuantityInStock in the product table
            query_update_quantity_in_stock = f"""
                UPDATE product
                SET QuantityInStock = QuantityInStock - {quantity_bought}
                WHERE ProductID = '{product_id}'
            """
            cursor.execute(query_update_quantity_in_stock)
            db.commit()

        st.success("Transaction recorded successfully!")
        # Clear the shopping cart after successful payment
        st.session_state.shopping_cart = []

# ... (previous code)

elif selected_tab == "Purchase History":
    # Display purchase history details
    st.title("Purchase History")

    if customer_info:
        # Fetch and display purchase history for the specific user
        query_purchase_history = f"""
            SELECT ph.purchase_id, ph.ProductID, p.Name, ph.QuantityBought, ph.PurchaseDate
            FROM purchase_history ph
            JOIN product p ON ph.ProductID = p.ProductID
            WHERE ph.customerid = '{user_id}'
        """
        cursor.execute(query_purchase_history)
        purchase_history = cursor.fetchall()

        if purchase_history:
            # Create a DataFrame for the purchase history
            import pandas as pd
            columns = ["Purchase ID", "Product ID", "Product Name", "Quantity Bought", "Purchase Date"]
            df = pd.DataFrame(purchase_history, columns=columns)

            # Display the purchase history table
            st.table(df)
        else:
            st.write("No purchase history found for this customer.")
    else:
        st.error("Customer not found in the database. Please check the ID.")

# ... (remaining code)
