from flask import Blueprint, render_template, request, url_for, flash, redirect, abort, session, current_app
import random

from app.utils import get_db_connection

# Create a blueprint for requests routes
requests_bp = Blueprint('requests', __name__,
                        template_folder='templates')


@requests_bp.route('/orders/')
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


# Function to get TMARequests entity by ID
def get_request_by_id(request_id):
    conn = get_db_connection()
    request_info = conn.execute('SELECT * FROM TMARequests WHERE RequestID = ?', (request_id,)).fetchone()
    conn.close()
    return request_info


def generate_employee_name():
    """
    Generate a default employee name for the order.
    In a real-world scenario, this function would retrieve the logged-in user's name or ID.
    As authorization is not implemented, it returns a random name.
    """
    first_names = ['John', 'Jane', 'Alice', 'Bob', 'Charlie', 'Emma', 'Ethan', 'Olivia', 'Noah', 'Sophia']
    last_names = ['Smith', 'Johnson', 'Williams', 'Brown', 'Jones', 'Garcia', 'Miller', 'Davis', 'Martinez', 'Clark']
    random_first_name = random.choice(first_names)
    random_last_name = random.choice(last_names)

    # Concatenate first and last name to form the full name
    full_name = f'{random_first_name} {random_last_name}'

    return full_name

@requests_bp.route('/orders/create/<int:item_id>', methods=['GET', 'POST'])
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
            
            employee_name = generate_employee_name()
            
            cursor.execute("""
                INSERT INTO TMARequests (EmployeeName, ItemID, UnitOfMeasurement, Quantity, PriceWithoutVAT, Comment)
                VALUES (?, ?, ?, ?, ?, ?)
            """, (employee_name, item_id, item['UnitOfMeasurement'], quantity, item['PriceWithoutVAT'], comment))
            request_id = cursor.lastrowid
            conn.commit()
            conn.close()

            flash('Request created', 'success')
            return redirect(url_for('routes.requests.list_orders'))

    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Items WHERE ItemID = ?", (item_id,))
    item = cursor.fetchone()
    conn.close()

    return render_template('order_item.html', item=item)



@requests_bp.route('/orders/order/<int:request_id>', methods=['GET', 'POST'])
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
        return redirect(url_for('routes.requests.purchase_requests'))

    conn = get_db_connection()
    request_info = conn.execute('SELECT * FROM TMARequests WHERE RequestID = ?', (request_id,)).fetchone()
    items = conn.execute('SELECT * FROM Items WHERE ItemID = ?', (request_id,)).fetchall()
    conn.close()

    if request_info is None:
        flash('Purchase request not found.', 'error')
        return redirect(url_for('routes.requests.purchase_requests'))

    return render_template('view_purchase_request.html', request_info=request_info, items=items)



@requests_bp.route('/orders/confirm/<int:request_id>/', methods=['POST'])
def confirm_purchase_request(request_id):
    request_info = get_request_by_id(request_id)
    if request_info is None:
        flash('Purchase request not found', 'error')
        return redirect(url_for('routes.requests.list_orders'))

    # Update the status to "Accepted" in the TMARequests table
    conn = get_db_connection()
    conn.execute('UPDATE TMARequests SET Status = ? WHERE RequestID = ?', ('Accepted', request_id))
    conn.commit()

    # Reduce the quantity in the Items table
    item_id = request_info['ItemID']
    quantity_requested = request_info['Quantity']

    conn = get_db_connection()
    item = conn.execute('SELECT * FROM Items WHERE ItemID = ?', (item_id,)).fetchone()
    if item is not None:
        updated_quantity = item['Quantity'] - quantity_requested
        conn.execute('UPDATE Items SET Quantity = ? WHERE ItemID = ?', (updated_quantity, item_id))
        conn.commit()
    conn.close()

    # Perform any additional logic here

    flash('Purchase request confirmed successfully', 'success')
    return redirect(url_for('routes.requests.list_orders'))



@requests_bp.route('/orders/reject/<int:request_id>/', methods=['POST'])
def reject_purchase_request(request_id):
    # Get reject comment from the form
    comment = request.form.get('comment')
    
    # Update the status and comment for the purchase request
    conn = get_db_connection()
    conn.execute('UPDATE TMARequests SET Status = ?, Comment = ? WHERE RequestID = ?', ('Rejected', comment, request_id))
    conn.commit()
    conn.close()

    flash('Purchase request rejected with comment: {}'.format(comment), 'success')
    return redirect(url_for('routes.requests.list_orders'))
