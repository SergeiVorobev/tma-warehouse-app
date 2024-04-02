from flask import render_template, request, redirect, url_for
from . import employee_bp
from run import conn

@employee_bp.route('/orders')
def employee_orders():
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM Items")
    items = cursor.fetchall()
    return render_template('employee/all_goods.html', items=items)

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
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Orders (item_name, unit_of_measurement, quantity, price_without_vat, comment)
            VALUES (?, ?, ?, ?, ?)
        """, (item_name, unit_of_measurement, quantity, price_without_vat, comment))
        conn.commit()
        cursor.close()

        return redirect(url_for('index'))

    # If method is GET, render the order form
    return render_template('employee/order.html')
