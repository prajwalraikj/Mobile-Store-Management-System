# Mobile-Store-Management-System
# DBMS Project

## Overview

This is a database management system (DBMS) project for managing customer transactions, purchase history, and product details. The project is developed using Python, MySQL, and Streamlit.

## Features

- **Product Management:** View and manage product details, including name, price, quantity in stock, and more.

- **Customer Management:** Maintain customer information, including name, contact information, address, loyalty points, and purchase history.

- **Transaction History:** Track customer transactions, including date and time, total amount, payment method, and employee involved.

- **Shopping Cart:** Allow customers to add products to a shopping cart, view the cart, and make payments.

- **Purchase History:** Display a history of customer purchases, including product details, quantity bought, and purchase date.

## Setup

1. **Database Setup:**
   - Create a MySQL database named `dbms_project`.
   - Execute the SQL script in `database_setup.sql` to create the necessary tables.

2. **Python Environment:**
   - Install the required Python packages using `pip install -r requirements.txt`.

3. **Run the Application:**
   - Execute `streamlit run customer.py` to launch the Streamlit web application.

## Project Structure

- **customer.py:** Main Python script for the Streamlit application.
- **database_setup.sql:** SQL script for setting up the initial database schema.

## Dependencies

- Python 3.10
- MySQL
- Streamlit
- MySQL Connector

## Contributing

Contributions are welcome! If you find any issues or have suggestions for improvements, please open an issue or create a pull request.

## License

This project is licensed under the [MIT License](LICENSE).
