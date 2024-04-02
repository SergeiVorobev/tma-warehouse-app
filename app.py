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
    conn = get_db_connection()
    goods = conn.execute('SELECT * FROM Items').fetchall()
    conn.close()
    return render_template('index.html', goods=goods)

def get_item(good_id):
    conn = get_db_connection()
    good = conn.execute('SELECT * FROM Items WHERE ItemID = ?',
                        (good_id,)).fetchone()
    conn.close()
    if good is None:
        abort(404)
    return good


@app.route('/create/', methods=('GET', 'POST'))
def create():
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
            return redirect(url_for('index'))

    return render_template('create.html')


@app.route('/<int:id>/edit/', methods=('GET', 'POST'))
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
            return redirect(url_for('index'))

    return render_template('edit.html', item=item)


@app.route('/<int:id>/delete/', methods=('POST',))
def delete(id):
    item = get_item(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM Items WHERE ItemID = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(item['ItemGroup']))
    return redirect(url_for('index'))
