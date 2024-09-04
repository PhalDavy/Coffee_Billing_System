from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

app = Flask(__name__)

# Database connection
def get_db_connection():
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='@dawin2003$',
        database='billing'
    )
    return connection

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_item', methods=['GET', 'POST'])
def add_item():
    if request.method == 'POST':
        item_id = request.form['itemID']
        item_name = request.form['itemName']
        category = request.form['category']
        size_option = request.form.get('sizeOption', None)
        price = request.form['price']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('InsertItem', [item_id, item_name, category, size_option, price])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('index'))

    return render_template('add_item.html')

@app.route('/edit_item/<string:item_id>', methods=['GET', 'POST'])
def edit_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)

    if request.method == 'POST':
        item_name = request.form['itemName']
        category = request.form['category']
        size_option = request.form.get('sizeOption', None)
        price = request.form['price']

        cursor.execute('''
            UPDATE items
            SET itemName = %s, category = %s, sizeOption = %s, price = %s
            WHERE itemID = %s
        ''', (item_name, category, size_option, price, item_id))
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('list_items'))

    cursor.execute('SELECT * FROM items WHERE itemID = %s', (item_id,))
    item = cursor.fetchone()
    cursor.close()
    conn.close()
    return render_template('edit_item.html', item=item)

@app.route('/delete_item/<string:item_id>', methods=['POST'])
def delete_item(item_id):
    conn = get_db_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('DELETE FROM order_items WHERE itemID = %s', (item_id,))
        cursor.callproc('DeleteItem', [item_id])
        conn.commit()
    except mysql.connector.Error as err:
        conn.rollback()
        print(f"Error: {err}")
    finally:
        cursor.close()
        conn.close()
    return redirect(url_for('list_items'))


@app.route('/view_order/<int:order_id>')
def view_order(order_id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.callproc('ViewOrder', [order_id])
    for result in cursor.stored_results():
        order_details = result.fetchall()
    cursor.close()
    conn.close()
    return render_template('view_order.html', order=order_details)

@app.route('/list_orders')
def list_orders():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM Orders')
    orders = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('list_orders.html', orders=orders)

@app.route('/add_order', methods=['GET', 'POST'])
def add_order():
    if request.method == 'POST':
        cashier_id = request.form['cashierID']
        item_ids = request.form.getlist('itemID')
        discounts = request.form.getlist('discount')
        quantities = request.form.getlist('quantity')

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('InsertOrder', [cashier_id, 0])
        conn.commit()
        cursor.execute('SELECT LAST_INSERT_ID()')
        order_id = cursor.fetchone()[0]

        for item_id, discount, quantity in zip(item_ids, discounts, quantities):
            cursor.callproc('InsertOrderItem', [order_id, item_id, discount, quantity])

        cursor.callproc('UpdateOrderTotalAmount', [order_id])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('view_order', order_id=order_id))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT cashierID, cashierName FROM Cashiers')
    cashiers = cursor.fetchall()
    cursor.execute('SELECT itemID, itemName FROM items')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('add_order.html', cashiers=cashiers, items=items)

@app.route('/add_order_items/<int:order_id>', methods=['GET', 'POST'])
def add_order_items(order_id):
    if request.method == 'POST':
        item_id = request.form['itemID']
        discount = request.form['discount']
        quantity = request.form['quantity']

        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.callproc('InsertOrderItem', [order_id, item_id, discount, quantity])
        conn.commit()
        cursor.callproc('UpdateOrderTotalAmount', [order_id])
        conn.commit()
        cursor.close()
        conn.close()
        return redirect(url_for('view_order', order_id=order_id))

    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT itemID, itemName FROM items')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('add_order_items.html', order_id=order_id, items=items)

@app.route('/list_items')
def list_items():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute('SELECT * FROM items')
    items = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('list_items.html', items=items)

if __name__ == '__main__':
    app.run(debug=True)
