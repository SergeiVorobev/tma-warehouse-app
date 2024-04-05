from flask import Flask, render_template, request, url_for, flash, redirect, abort, session
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


def get_item(good_id):
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
    item = get_item(id)

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
    item = get_item(id)
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


@app.route('/orders/create/<int:item_id>', methods=['GET', 'POST'])
def order_item(item_id):
    if request.method == 'POST':
        quantity = request.form['quantity']
        comment = request.form['comment']
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("SELECT * FROM Items WHERE ItemID = ?", (item_id,))
        item = cursor.fetchone()
        conn.close()
        # employee_name = session['employee_name']
        employee_name = 'Sergei'
        
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO TMARequests (EmployeeName, ItemID, UnitOfMeasurement, Quantity, PriceWithoutVAT, Comment)
            VALUES (?, ?, ?, ?, ?, ?)
        """, (employee_name, item_id, item['UnitOfMeasurement'], quantity, item['PriceWithoutVAT'], comment))
        request_id = cursor.lastrowid
        conn.commit()
        conn.close()

        flash('Request created', 'success')
        return redirect(url_for('list_items'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Items WHERE ItemID = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()

    return render_template('order_item.html', item=item)
