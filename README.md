Trade and Material Assets (TMA) Warehouse App
=============================================

Overview
--------
The Trade and Material Assets (TMA) Warehouse app is a web-based solution designed to manage goods, purchase requests, and inventory for businesses. It provides functionalities for coordinators to manage goods inventory and purchase requests, as well as for employees to submit purchase requests.

Features
--------
- **Coordinator Functions**:
  - View, add, update, and remove goods from inventory.
  - View, confirm, or reject purchase requests.
  - Search, filter, and sort goods and purchase requests.

- **Employee Functions**:
  - View the list of goods and purchase requests.
  - Submit purchase requests for required items.

Setup
-----
To set up the TMA Warehouse app locally, follow these steps:

1. Clone the repository:
git clone <repository_url>


2. Set up a virtual environment (optional but recommended):
python -m venv venv


3. Activate the virtual environment:
- On Windows:
  ```
  venv\Scripts\activate
  ```
- On macOS and Linux:
  ```
  source venv/bin/activate
  ```

4. Install dependencies:
pip install -r requirements.txt


5. Configure database connection:
- Update the database connection parameters in the `.env` file.

6. Initialize the database schema:
- Run the initialization script to create the necessary tables and relationships:
  ```
  python init_db.py
  ```

7. Start the application:
python run.py

alternatively yiu can run it with 
```
python -m flask run --port 5000 --debug
```

8. Access the application in your web browser:
http://localhost:5000


This setup guide assumes you have Python installed on your system. The project relies on Flask, a Python web framework, and uses Jinja2 templating for HTML rendering. The database schema is set up using SQLite by default, but you can configure other databases like MySQL or PostgreSQL by updating the `.env` file.

Contributing
------------
Contributions to the TMA Warehouse app are welcome! Please follow the guidelines outlined in the CONTRIBUTING.md file.

License
-------
This project is licensed under the [MIT License](LICENSE).
