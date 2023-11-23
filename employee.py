# employee.py

import os
import streamlit as st
import mysql.connector

# Retrieve employee_id from environment variable
employee_id = os.environ.get("USER_ID")

# Connect to the database and fetch employee information
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="dbms_project"
)
def set_discount(product_id, discount_value):
    try:
        cursor.callproc('set_discount', (product_id, discount_value))
        db.commit()
        st.success(f"Discount set successfully for product {product_id}.")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")

def set_discount_for_all_products(discount_value):
    try:
        cursor.callproc('set_discount_for_all', (discount_value,))
        db.commit()
        st.success("Discount set successfully for all products.")
    except mysql.connector.Error as err:
        st.error(f"Error: {err}")



cursor = db.cursor()
query_employee = f"SELECT * FROM Employee WHERE EmployeeID = '{employee_id}'"
cursor.execute(query_employee)
employee_info = cursor.fetchone()

# Print employee_info for debugging
print("Employee Info:", employee_info)

# Sidebar navigation
selected_tab = st.sidebar.radio("Navigation", ["Employee Profile", "Add Products","View Units Sold","Branch Details","View Finances","Set Discount","Update Information"])

def delete_employee(employee_id):
    """Deletes the employee from the database."""
    query_delete_employee = f"DELETE FROM Employee WHERE EmployeeID = '{employee_id}'"
    cursor.execute(query_delete_employee)
    db.commit()
    st.success("Employee deleted successfully!")

# Display content based on selected tab
if selected_tab == "Employee Profile":
    # Display employee information
    st.title("Employee Profile")
    if employee_info:
        st.markdown(f"*Employee ID:* {employee_info[0]}")
        st.markdown(f"*Name:* {employee_info[1]}")
        st.markdown(f"*Contact Information:* {employee_info[2]}")
        st.markdown(f"*Department:* {employee_info[3]}")
        st.markdown(f"*Salary:* {employee_info[4]}")

       

            # Display an empty space for better layout
        st.empty()

            

        # Delete button
        delete_employee_button = st.button("Delete Employee", key="delete_employee_button")
        if delete_employee_button:
            delete_employee(employee_id)
            st.balloons()  # Celebrate the deletion
            st.experimental_rerun()  # Refresh the page after deletion
    else:
        st.error("Employee not found in the database. Please check the ID.")



elif selected_tab == "Add Products":
    if employee_info and employee_info[3].strip() == "Management":
        st.title("Add Products")

        # Get product details from the user
        product_id = st.text_input("Enter Product ID:")
        name = st.text_input("Enter Product Name:")
        category = st.text_input("Enter Category:")
        price = st.number_input("Enter Price:", min_value=0.0)
        quantity_in_stock = st.number_input("Enter Quantity in Stock:", min_value=0)
        manufacturer = st.text_input("Enter Manufacturer:")
        description = st.text_area("Enter Description:")

        # Add the product to the database
        add_product_button = st.button("Add Product")

        if add_product_button:
            # Check if the product ID already exists
            query_check_product = f"SELECT * FROM Product WHERE ProductID = '{product_id}'"
            cursor.execute(query_check_product)
            existing_product = cursor.fetchone()

            if existing_product:
                st.warning("Product ID already exists. Please use a different ID.")
            else:
                # Insert the new product into the Product table
                query_add_product = f"INSERT INTO Product (ProductID, Name, Category, Price, QuantityInStock, Manufacturer, Description) VALUES ('{product_id}', '{name}', '{category}', {price}, {quantity_in_stock}, '{manufacturer}', '{description}')"
                cursor.execute(query_add_product)
                db.commit()
                st.success("Product added successfully!")

                # Ask if the employee wants to add another product
                add_another_product = st.checkbox("Add another product?")
                if not add_another_product:
                    st.info("You can always come back to add more products.")
    else:
        # Debugging statement
        st.warning(f"Employee does not have permission for tab '{selected_tab}'. Department: {employee_info[3].strip()}")

# ... (remaining code)


elif selected_tab=="View Units Sold":
    if employee_info and (employee_info[3].strip() == "Sales" or employee_info[3].strip() == "Management"):
        st.title("View Units Sold")

        # Debugging statement
        st.write("Employee has permission to access View Units Sold tab.")
    
    else:
        # Debugging statement
        st.warning(f"Employee does not have permission for tab '{selected_tab}'. Department: {employee_info[3].strip()}")

elif selected_tab == "Branch Details":
    st.title("Branch Details")

    # Get branch ID from the user
    branch_id = st.text_input("Enter Store Branch ID:")
    get_branch_info_button = st.button("Get Branch Details")

    if get_branch_info_button:
        # Connect to the database and fetch store branch information
        query_branch = f"SELECT * FROM storebranch WHERE storebranchid = '{branch_id}'"
        cursor.execute(query_branch)
        branch_info = cursor.fetchone()

        # Display branch information
        if branch_info:
            st.markdown(f"*Branch ID:* {branch_info[0]}")
            st.markdown(f"*Location:* {branch_info[1]}")
            st.markdown(f"*Manager:* {branch_info[3]}")
            st.markdown(f"*Contact Information:* {branch_info[2]}")
            st.markdown(f"*Opening Hours:* {branch_info[4]}")
            # Add more details as needed
        else:
            st.error("Store branch not found. Please check the branch ID.")

# ... (previous code)

# ... (previous code)

elif selected_tab == "View Finances":
    if employee_info and (employee_info[3].strip() == "Management" or employee_info[3].strip() == "Finance" or employee_info[3].strip() == "Sales"):
        st.title("View Finances")

        # Nested query to fetch total revenue from the Transaction table
        query_finances = f"""
            SELECT SUM(TotalAmount) 
            FROM Transaction 
            WHERE customerid IN (
                SELECT customerid 
                FROM Customer 
                WHERE employeeid = '{employee_id}'
            )
        """
        cursor.execute(query_finances)
        total_revenue = cursor.fetchone()[0]

        # Display total revenue
        st.write(f"Total Revenue: {total_revenue}")

        # Fetch average transaction amount from the Transaction table for the transactions associated with the current employee's customers
        query_average_transaction = f"""
        SELECT AVG(TotalAmount)
        FROM Transaction
        WHERE customerid IN (SELECT customerid FROM Customer WHERE employeeid = '{employee_id}')
        """
        cursor.execute(query_average_transaction)
        average_transaction_amount = cursor.fetchone()[0]

        # Display average transaction amount
        st.write(f"Average Transaction Amount: {average_transaction_amount}")

        # Bar chart to compare revenue per employee
        # Bar chart to compare revenue per employee
        query_revenue_per_employee = f"""
            SELECT e.Name AS EmployeeName, SUM(t.TotalAmount) AS TotalRevenue
            FROM Transaction t
            JOIN Customer c ON t.customerid = c.customerid
            JOIN Employee e ON t.employeeid = e.employeeid
            WHERE t.employeeid = '{employee_id}'
            GROUP BY e.employeeid
        """
        cursor.execute(query_revenue_per_employee)
        revenue_data = cursor.fetchall()


        # Create a DataFrame for the revenue data
        import pandas as pd
        revenue_df = pd.DataFrame(revenue_data, columns=["EmployeeName", "TotalRevenue"])

        # Display the bar chart
        st.bar_chart(revenue_df.set_index("EmployeeName"))

        # Add more financial details or visualization as needed
    else:
        st.warning(f"Employee does not have permission for tab '{selected_tab}'. Department: {employee_info[3].strip()}")

# ... (remaining code)


elif selected_tab == "Set Discount":
    # Check if the employee belongs to the Management department
    if employee_info and employee_info[3].strip() == "Management":
        # Display UI for setting the discount
        st.title("Set Discount")

        # Option to set discount for a specific product
        product_id_to_set_discount = st.text_input("Enter Product ID to set discount for a specific product:")
        specific_product_discount_value = st.number_input("Enter Discount Value for the specific product:", min_value=0.0)

        # Option to set discount for all products
        set_discount_for_all = st.checkbox("Set Discount for All Products")
        all_products_discount_value = st.number_input("Enter Discount Value for all products:", min_value=0.0)

        set_discount_button = st.button("Set Discount")

        if set_discount_button:
            if product_id_to_set_discount and specific_product_discount_value:
                # Call the set_discount stored procedure for a specific product
                set_discount(product_id_to_set_discount, specific_product_discount_value)
                st.success(f"Discount set successfully for product {product_id_to_set_discount}.")

            if set_discount_for_all and all_products_discount_value:
                # Call the set_discount stored procedure for all products
                set_discount_for_all_products(all_products_discount_value)
                st.success("Discount set successfully for all products.")
    else:
        st.warning("You do not have permission to set the discount. Only Management department can set the discount.")


elif selected_tab=="Update Information":
     # Update button
    field_to_update = st.selectbox("Select Field to Update", ["Name", "ContactInformation", "Department", "Salary"])
    new_value = st.text_input(f"Enter New {field_to_update}:")
    update_employee_button = st.button("Update Employee Information", key="update_employee_info_button")
        
    if update_employee_button:
        query_update_employee = f"UPDATE Employee SET {field_to_update} = '{new_value}' WHERE EmployeeID = '{employee_id}'"
        cursor.execute(query_update_employee)
        db.commit()
        st.success(f"Employee {field_to_update} updated successfully!")
    else:
        st.warning("Please enter both the field and new value.")

    """Updates a specific field for the employee in the database."""
    

# ... (remaining code)
