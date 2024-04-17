from flask import Flask, render_template, request, url_for, flash, redirect, abort
import sqlite3

from config import Config

app = Flask(__name__)
app.secret_key = Config.SECRET_KEY

def get_db_connection():
    conn = sqlite3.connect('db/database.db')
    conn.row_factory = sqlite3.Row
    return conn


@app.route('/')
def index():
    return render_template('base.html')


@app.route('/items/')
def list_items():
    conn = get_db_connection()
    goods = conn.execute('SELECT * FROM Items').fetchall()
    conn.close()
    return render_template('list_items.html', goods=goods)


def get_items(good_id):
    conn = get_db_connection()
    good = conn.execute('SELECT * FROM Items WHERE ItemID = ?',
                        (good_id,)).fetchone()
    conn.close()
    if good is None:
        abort(404)
    return good


@app.route('/items/create/', methods=('GET', 'POST'))
def create_item():
    if request.method == 'POST':
        item_group = request.form['item_group']
        unit_of_measurement = request.form['unit_of_measurement']
        quantity = request.form['quantity']
        price_without_vat = request.form['price_without_vat']
        status = request.form['status']
        storage_location = request.form['storage_location']
        contact_person = request.form['contact_person']
        photo_file_path = request.form['photo_file_path']

        if not item_group:
            flash('Item group is required!')
        elif not unit_of_measurement:
            flash('Unit of measurement is required!')
        elif not quantity:
            flash('Quantity is required!')
        elif not price_without_vat:
            flash('Price without VAT is required!')
        elif not status:
            flash('Status is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('INSERT INTO Items (ItemGroup, UnitOfMeasurement, Quantity, PriceWithoutVAT, Status, StorageLocation, ContactPerson, PhotoFilePath) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                         (item_group, unit_of_measurement, quantity, price_without_vat, status, storage_location, contact_person, photo_file_path))
            conn.commit()
            cursor.close()
            conn.close()
            flash('Item added successfully', 'success')
            return redirect(url_for('list_items'))

    return render_template('create_item.html')


@app.route('/items/edit/<int:id>/', methods=('GET', 'POST'))
def edit_item(id):
    item = get_items(id)

    if request.method == 'POST':
        item_group = request.form['item_group']
        unit_of_measurement = request.form['unit_of_measurement']
        quantity = request.form['quantity']
        price_without_vat = request.form['price_without_vat']
        status = request.form['status']
        storage_location = request.form['storage_location']
        contact_person = request.form['contact_person']
        photo_file_path = request.form['photo_file_path']

        if not item_group:
            flash('Item group is required!')
        elif not unit_of_measurement:
            flash('Unit of measurement is required!')
        elif not quantity:
            flash('Quantity is required!')
        elif not price_without_vat:
            flash('Price without VAT is required!')
        elif not status:
            flash('Status is required!')
        else:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute('UPDATE Items SET ItemGroup = ?, UnitOfMeasurement = ?, Quantity = ?, PriceWithoutVAT = ?, Status = ?, StorageLocation = ?, ContactPerson = ?, PhotoFilePath = ? WHERE ItemID = ?',
                         (item_group, unit_of_measurement, quantity, price_without_vat, status, storage_location, contact_person, photo_file_path, id))
            conn.commit()
            conn.close()
            flash('Item updated successfully', 'success')
            return redirect(url_for('list_items'))

    return render_template('edit_item.html', item=item)


@app.route('/items/delete/<int:id>/', methods=('POST',))
def delete_item(id):
    item = get_items(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM Items WHERE ItemID = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(item['ItemGroup']))
    return redirect(url_for('list_items'))


@app.route('/orders/')
def list_orders():
    conn = get_db_connection()
    requests = conn.execute('SELECT * FROM TMARequests').fetchall()
    conn.close()
    return render_template('list_orders.html', requests=requests)


# Function to get the available quantity of an item from the Items table
def get_available_quantity(item_id, new_quantity=None, check_available=True):
    conn = get_db_connection()
    item_info = conn.execute('SELECT * FROM Items WHERE ItemID = ?', (item_id,)).fetchone()
    available_quantity = int(item_info['Quantity'])
    conn.close()

    if check_available and new_quantity is not None:
        new_quantity = int(new_quantity)
        if new_quantity > available_quantity:
            flash('Quantity exceeds available stock', 'error')
            return False, available_quantity
    return True, available_quantity


@app.route('/orders/create/<int:item_id>', methods=['GET', 'POST'])
def order_item(item_id):
    if request.method == 'POST':
        quantity = request.form['quantity']
        comment = request.form['comment']
        
        check_available, available_quantity = get_available_quantity(item_id, quantity)
        if check_available:
            conn = get_db_connection()
            cursor = conn.cursor()
            cursor.execute("SELECT * FROM Items WHERE ItemID = ?", (item_id,))
            item = cursor.fetchone()
            
            employee_name = 'Sergei'
            
            cursor.execute("""
                INSERT INTO TMARequests (EmployeeName, ItemID, UnitOfMeasurement, Quantity, PriceWithoutVAT, Comment)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (employee_name, item_id, item['UnitOfMeasurement'], quantity, item['PriceWithoutVAT'], comment))
            request_id = cursor.lastrowid
            conn.commit()
            conn.close()

            flash('Request created', 'success')
            return redirect(url_for('list_orders'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Items WHERE ItemID = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()

    return render_template('order_item.html', item=item)


@app.route('/orders/order/<int:request_id>', methods=['GET', 'POST'])
def view_purchase_request(request_id):
    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'confirm':
            # Logic to confirm the request
            flash('Request confirmed', 'success')
        elif action == 'reject':
            # Logic to reject the request
            comment = request.form.get('comment')
            flash('Request rejected with comment: {}'.format(comment), 'error')
        return redirect(url_for('purchase_requests'))

    conn = get_db_connection()
    request_info = conn.execute('SELECT * FROM TMARequests WHERE RequestID = ?', (request_id,)).fetchone()
    items = conn.execute('SELECT * FROM TMARequestRows WHERE RequestID = ?', (request_id,)).fetchall()
    conn.close()

    if request_info is None:
        flash('Purchase request not found.', 'error')
        return redirect(url_for('purchase_requests'))

    return render_template('view_purchase_request.html', request_info=request_info, items=items)


# Function to get TMARequests entity by ID
def get_request_by_id(request_id):
    conn = get_db_connection()
    request_info = conn.execute('SELECT * FROM TMARequests WHERE RequestID = ?', (request_id,)).fetchone()
    conn.close()
    return request_info


@app.route('/orders/update_quantity/<int:request_id>/', methods=['POST'])
def update_quantity(request_id):
    if request.method == 'POST':
        new_quantity = int(request.form['quantity'])

        # Get the request information
        request_info = get_request_by_id(request_id)
        if not request_info:
            flash('Request not found', 'error')
            return redirect(url_for('list_orders'))

        # Get the available quantity of the item
        item_id = request_info['ItemID']
        available, available_quantity = get_available_quantity(item_id, new_quantity)
        if not available:
            flash('Quantity exceeds available stock', 'error')
            return redirect(url_for('view_purchase_request', request_id=request_id))

        # Update the quantity in the purchase request
        conn = get_db_connection()
        conn.execute('UPDATE TMARequests SET Quantity = ? WHERE RequestID = ?', (new_quantity, request_id))
        conn.commit()

        # Retrieve updated item information from TMARequests
        updated_item_info = get_request_by_id(request_id)
        conn.close()

        flash('Quantity updated successfully', 'success')

    return redirect(url_for('view_purchase_request', request_id=request_id))


# Route for confirming a purchase request
@app.route('/orders/confirm/<int:request_id>/', methods=['POST'])
def confirm_purchase_request(request_id):
    # Logic to confirm the purchase request
    request_info = get_request_by_id(request_id)
    if request_info is None:
        flash('Purchase request not found', 'error')
        return redirect(url_for('list_orders'))

    # Perform any additional logic here

    flash('Purchase request confirmed successfully', 'success')
    return redirect(url_for('list_orders'))

# Route for rejecting a purchase request
@app.route('/orders/reject/<int:request_id>/', methods=['POST'])
def reject_purchase_request(request_id):
    # Logic to reject the purchase request
    comment = request.form.get('comment')
    request_info = get_request_by_id(request_id)
    if request_info is None:
        flash('Purchase request not found', 'error')
        return redirect(url_for('list_orders'))

    # Perform any additional logic here

    flash('Purchase request rejected with comment: {}'.format(comment), 'success')
    return redirect(url_for('list_orders'))
