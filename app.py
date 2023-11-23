import streamlit as st
import subprocess
import mysql.connector
import os

# Establish a connection to the database
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="password",
    database="dbms_project"
)
cursor = db.cursor()


def id_exists(user_id, user_type):
    """Checks if a user with the given ID exists in the database."""
    query = f"SELECT * FROM {user_type} WHERE {user_type}ID = '{user_id}'"
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="dbms_project"
    )
    cursor = db.cursor()
    cursor.execute(query)
    result = cursor.fetchone()
    return result is not None

def signup_customer():
    st.title("Customer Sign Up")

    customer_id = st.text_input("Enter Customer ID (starts with 'C'):")
    name = st.text_input("Enter Name:")
    contact_info = st.text_input("Enter Contact Information:")
    address = st.text_input("Enter Address:")
    password = st.text_input("Enter password:")

    # Check if the customer_id starts with 'C'
    if not customer_id.startswith("C"):
        st.error("Customer ID must start with 'C'. Please enter a valid ID.")
        return

    # Check if the customer ID already exists in the database
    if id_exists(customer_id, "Customer"):
        st.warning("Customer ID already exists. Please login or use a different ID.")
        return

    # Add a unique key to the signup button
    signup_button = st.button("Sign Up Customer", key="signup_customer_button_" + customer_id)

    if signup_button:
        # Insert new customer into the database
        query = f"INSERT INTO Customer (CustomerID, Name, ContactInformation, Address, Password) VALUES ('{customer_id}', '{name}', '{contact_info}', '{address}', '{password}')"
        execute_query(query, "Customer")


def signup_employee():
    st.title("Employee Sign Up")

    employee_id = st.text_input("Enter Employee ID (starts with 'E'):")
    name = st.text_input("Enter Name:")
    contact_info = st.text_input("Enter Contact Information:")
    department = st.text_input("Enter Department:")
    salary = st.number_input("Enter Salary:", min_value=0)
    password = st.text_input("Enter password:")

    # Check if the employee_id starts with 'E'
    if not employee_id.startswith("E"):
        st.error("Employee ID must start with 'E'. Please enter a valid ID.")
        return

    # Check if the employee ID already exists in the database
    if id_exists(employee_id, "Employee"):
        st.warning("Employee ID already exists. Please login or use a different ID.")
        return

    # Add a unique key to the signup button
    signup_button = st.button("Sign Up Employee", key="signup_employee_button_" + employee_id)

    if signup_button:
        # Insert new employee into the database
        query = f"INSERT INTO Employee (EmployeeID, Name, ContactInformation, Department, Salary, Password) VALUES ('{employee_id}', '{name}', '{contact_info}', '{department}', {salary}, '{password}')"
        execute_query(query, "Employee")

def execute_query(query, user_type):
    # Connect to the database and execute the query
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="password",
        database="dbms_project"
    )
    cursor = db.cursor()
    cursor.execute(query)
    db.commit()
    st.success(f"{user_type} signed up successfully!")

def login():
    # Use st.session_state to store the customer ID and redirect flag
    if 'user_id' not in st.session_state:
        st.session_state.user_id = None

    # Use st.text_input to set the default value based on session_state
    user_id = st.text_input("Enter Customer/Employee ID:", key="login_user_id", value=st.session_state.user_id)
    password = st.text_input("Enter Password:", type="password")

    # Add a unique key to the login button
    # Add a unique key to the login button
    login_button = st.button("Login", key="login_button")

    if login_button:
        # Perform the login check in the database
        if user_id.startswith("C"):
            # Check in the Customer table
            query = f"SELECT * FROM Customer WHERE CustomerID = '{user_id}' AND Password = '{password}'"
            # Set the user ID in the environment variable for customer
            os.environ["USER_ID"] = user_id  # Change this to USER_ID
            print("User ID set in environment variable:", os.environ["USER_ID"])
        elif user_id.startswith("E"):
            # Check in the Employee table
            query = f"SELECT * FROM Employee WHERE EmployeeID = '{user_id}' AND Password = '{password}'"
            # Set the user ID in the environment variable for employee
            os.environ["USER_ID"] = user_id  # Change this to USER_ID
            print("User ID set in environment variable:", os.environ["USER_ID"])
        else:
            st.error("Invalid User ID format. Please use 'C' for Customer or 'E' for Employee.")
            return


        # Connect to the database and execute the query
        db = mysql.connector.connect(
            host="localhost",
            user="root",
            password="password",
            database="dbms_project"
        )
        cursor = db.cursor()
        cursor.execute(query)
        result = cursor.fetchone()

        # Check if login was successful
        if result:
            st.success("Login successful!")

            # Run the corresponding script using subprocess
            if user_id.startswith("C"):
                subprocess.run(["streamlit", "run", "customer.py"], check=True)
            elif user_id.startswith("E"):
                subprocess.run(["streamlit", "run", "employee.py"], check=True)

def main():
    st.title("Mobile Store Management System")

    # Centered buttons
    st.markdown("<h2 style='text-align: center;'>Welcome to the Homepage</h2>", unsafe_allow_html=True)

    # Center the buttons
    col1, col2, col3 = st.columns(3)

    # Login/Signup button
    with col2:
        action_choice = st.sidebar.radio("Choose Action", ["Login", "Signup"])

    if action_choice == "Login":
        login()
    elif action_choice == "Signup":
        signup_choice = st.selectbox("Sign Up As", ["Select", "Customer", "Employee"])

        if signup_choice == "Customer":
            signup_customer()
        elif signup_choice == "Employee":
            signup_employee()
        elif signup_choice == "Select":
            st.warning("Please select a user type to sign up.")

if __name__ == "__main__":
    main()
