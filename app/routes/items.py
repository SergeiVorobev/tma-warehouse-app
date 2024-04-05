from flask import Blueprint, render_template, request, url_for, flash, redirect, abort, session

from app.utils import get_db_connection

items_bp = Blueprint('items', __name__,
                     template_folder='templates')


@items_bp.route('/items/')
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


@items_bp.route('/items/create/', methods=['GET', 'POST'])
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

        # Update status to default to 'New' if not provided
        if not status:
            status = 'New'

        if not item_group:
            flash('Item group is required!')
        elif not unit_of_measurement:
            flash('Unit of measurement is required!')
        elif not quantity:
            flash('Quantity is required!')
        elif not price_without_vat:
            flash('Price without VAT is required!')
        else:
            # Check if the provided status is valid
            valid_statuses = ['New', 'Approve', 'Reject']
            if status not in valid_statuses:
                flash('Invalid status provided!')
            else:
                conn = get_db_connection()
                cursor = conn.cursor()
                cursor.execute('INSERT INTO Items (ItemGroup, UnitOfMeasurement, Quantity, PriceWithoutVAT, Status, StorageLocation, ContactPerson, PhotoFilePath) VALUES (?, ?, ?, ?, ?, ?, ?, ?)',
                             (item_group, unit_of_measurement, quantity, price_without_vat, status, storage_location, contact_person, photo_file_path))
                conn.commit()
                cursor.close()
                conn.close()
                flash('Item added successfully', 'success')
                return redirect(url_for('routes.items.list_items'))

    return render_template('create_item.html')



@items_bp.route('/items/edit/<int:id>/', methods=['GET', 'POST'])
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
            return redirect(url_for('routes.items.list_items'))

    return render_template('edit_item.html', item=item)

@items_bp.route('/items/delete/<int:id>/', methods=['POST'])
def delete_item(id):
    item = get_items(id)
    conn = get_db_connection()
    conn.execute('DELETE FROM Items WHERE ItemID = ?', (id,))
    conn.commit()
    conn.close()
    flash('"{}" was successfully deleted!'.format(item['ItemGroup']))
    return redirect(url_for('routes.items.list_items'))
