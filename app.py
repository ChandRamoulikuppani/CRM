from flask import Flask, render_template, request, redirect, flash
import sqlite3

app = Flask(__name__)
app.secret_key = 'your_secret_key'  # Necessary for flash messages

def get_db_connection():
    conn = sqlite3.connect('customers.db')
    conn.row_factory = sqlite3.Row
    return conn

@app.route('/')
def index():
    conn = get_db_connection()
    customers = conn.execute('SELECT * FROM customers').fetchall()
    conn.close()
    return render_template('index.html', customers=customers)

@app.route('/add_customer', methods=('GET', 'POST'))
def add_customer():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        conn = get_db_connection()
        try:
            conn.execute('INSERT INTO customers (name, email, phone) VALUES (?, ?, ?)',
                         (name, email, phone))
            conn.commit()
            flash('Customer added successfully!', 'success')
            return redirect('/')
        except sqlite3.IntegrityError:
            flash('Customer data is already available with this email. Please enter a different email.', 'error')
        finally:
            conn.close()
    
    return render_template('customer_form.html')

@app.route('/delete_customer/<int:customer_id>', methods=('POST',))
def delete_customer(customer_id):
    try:
        conn = get_db_connection()
        conn.execute('DELETE FROM customers WHERE id = ?', (customer_id,))
        conn.commit()
        flash('Customer deleted successfully.', 'success')
    except Exception as e:
        flash('An error occurred while deleting the customer: ' + str(e), 'error')
    finally:
        conn.close()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True)
