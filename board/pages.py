from flask import Blueprint, render_template, request, redirect, url_for, flash
import sqlite3
from sqlite3 import Error


bp = Blueprint("pages", __name__)
coordinator_bp = Blueprint('coordinator', __name__)
employee_bp = Blueprint('employee', __name__)

def connect_db():
    conn = None
    try:
        conn = sqlite3.connect('db/database.db')
        conn.row_factory = sqlite3.Row
    except Error as e:
        print(e)

    return conn

def get_goods():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Items")
    goods = cursor.fetchall()
    cursor.close()
    conn.close()
    return goods

def get_purchase_requests():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM TMARequests")
    requests = cursor.fetchall()
    cursor.close()
    conn.close()
    return requests

@bp.route("/")
def home():
    return render_template("pages/home.html")

@bp.route("/about")
def about():
    return render_template("pages/about.html")

@coordinator_bp.route('/goods', methods=['GET', 'POST'])
def coordinator_goods():
    if request.method == 'POST':
        # Redirect to the add_item route for item insertion
        return redirect(url_for('coordinator.add_item'))
    
    # Handling GET request to display list of goods and the form to add new items
    goods = get_goods()
    
    return render_template('coordinator/goods.html', goods=goods)


@coordinator_bp.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        try:
            # Handling the addition of new items
            item_group = request.form['item_group']
            unit_of_measurement = request.form['unit_of_measurement']
            quantity = request.form['quantity']
            price_without_vat = request.form['price_without_vat']
            status = request.form['status']
            storage_location = request.form['storage_location']
            contact_person = request.form['contact_person']
            photo_file_path = request.form['photo_file_path']

            # Insert item into database
            with open('db/schema.sql') as f:
                conn = connect_db()
                conn.executescript(f.read())
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO Items (ItemGroup, UnitOfMeasurement, Quantity, PriceWithoutVAT, Status, StorageLocation, ContactPerson, PhotoFilePath)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (item_group, unit_of_measurement, quantity, price_without_vat, status, storage_location, contact_person, photo_file_path))
                conn.commit()
                cursor.close()
                conn.close()
                flash('Item added successfully', 'success')
            return redirect(url_for('coordinator.coordinator_goods'))
        except Exception as e:
            flash(f'Error adding item: {str(e)}', 'error')
            return redirect(url_for('coordinator.coordinator_goods'))

    # Rendering the form to add a new item
    return render_template('coordinator/add_good.html')

@coordinator_bp.route('/update_item/<int:item_id>', methods=['GET', 'POST'])
def update_item(item_id):
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Items WHERE ItemID = ?", (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()

    if request.method == 'POST':
        # Get form data
        item_group = request.form['item_group']
        unit_of_measurement = request.form['unit_of_measurement']
        quantity = request.form['quantity']
        price_without_vat = request.form['price_without_vat']
        status = request.form['status']
        storage_location = request.form['storage_location']
        contact_person = request.form['contact_person']
        photo_file_path = request.form['photo_file_path']

        # Update item in the database (implement this)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
            UPDATE Items 
            SET ItemGroup=?, UnitOfMeasurement=?, Quantity=?, PriceWithoutVAT=?, Status=?, StorageLocation=?, ContactPerson=?, PhotoFilePath=?
            WHERE ItemID=?
        """, (item_group, unit_of_measurement, quantity, price_without_vat, status, storage_location, contact_person, photo_file_path, item_id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Item updated successfully', 'success')
        return redirect(url_for('coordinator.all_goods'))

    return render_template('coordinator/update_item.html', item=item)


@coordinator_bp.route('/delete_item/<int:item_id>', methods=['POST'])
def delete_item(item_id):
    # Delete item from the database (implement this)
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Items WHERE ItemID = ?", (item_id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Item deleted successfully', 'success')  # Flash message for successful operation
    return redirect(url_for('coordinator.coordinator_goods'))


@coordinator_bp.route('/purchase_requests', methods=['GET', 'POST'])
def coordinator_purchase_requests():
    requests = get_purchase_requests()
    return render_template('coordinator/purchase_requests.html', requests=requests)


@employee_bp.route('/orders')
def employee_orders():
    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Items")
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('coordinator/all_goods.html', items=items)

# Route to handle ordering of goods by the employee
@employee_bp.route('/order', methods=['GET', 'POST'])
def order():
    if request.method == 'POST':
        # Get form data
        item_name = request.form['item_name']
        unit_of_measurement = request.form['unit_of_measurement']
        quantity = request.form['quantity']
        price_without_vat = request.form['price_without_vat']
        comment = request.form['comment']

        # Insert order into database (implement this)
        conn = connect_db()
        cursor = conn.cursor()
        cursor.execute("""
             INSERT INTO TMARequests (EmployeeName, ItemID, UnitOfMeasurement, Quantity, PriceWithoutVAT, Comment)
            VALUES (?, ?, ?, ?, ?, ?)
        """, ('Employee Name', item_name, unit_of_measurement, quantity, price_without_vat, comment))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('employee.order'))

    # If method is GET, render the order form
    return render_template('employee/order.html')
