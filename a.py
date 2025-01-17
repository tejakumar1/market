from flask import Flask, request, render_template, redirect, url_for
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import os
from jinja2 import Environment, FileSystemLoader

app = Flask(__name__)

# Function to send the order email
def send_order_email(customer_email, order_details):
    sender_email = os.getenv("SENDER_EMAIL","tejakumar2121@gmail.com")
    sender_password = os.getenv("SENDER_PASSWORD","ifmwbxgycvsaqwbv")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = customer_email
    message["Subject"] = "Your Order Details"

    body = f"WE got an new ORDER . Here are your details:\n\n{order_details}"
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
    except Exception as e:
        print(f"Error: {e}")

# Route to render the HTML form
@app.route('/')
def order_form():
    return render_template('main.html')  # Make sure your HTML is saved as 'templates/index.html'

# Route to handle form submission
@app.route('/submit-order', methods=['POST'])
def submit_order():
    name = request.form['customer-name']
    email = request.form['customer-email']
    phone = request.form['customer-phone']
    vegetable = request.form['item-select-vegetable']
    fruit = request.form['item-select-fruit']
    meat = request.form['item-select-meat']
    quantity = request.form['quantity']

    # Format the order details for the email
    order_details = f"""
    Name: {name}
    Email: {email}
    Phone: {phone}
    Vegetable: {vegetable}
    Fruit: {fruit}
    Meat: {meat}
    Quantity: {quantity}
    """
    print( order_details)

    # Send the order email
    send_order_email(email, order_details)


    return redirect(url_for('order_confirmation', name=name))

# Route to display the order confirmation page
@app.route('/confirmation-details')
def order_confirmation():
    name = request.args.get('name')

    return f"<h1>Thank you, {name}! Your order has been placed successfully.</h1>"

if __name__ == '__main__':
    app.run(debug=True)







from flask import Flask, request, render_template, jsonify
import mysql.connector
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask import Flask, request, render_template, redirect, url_for
load_dotenv()

app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True

# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'market'
}

# Function to insert order data into the database
def insert_order_data(order_data):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = """
        INSERT INTO order (name, email, phone, vegetables, fruits, meats, quantity)
        VALUES (%s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            order_data['name'],
            order_data['email'],
            order_data['phone'],
            ', '.join(order_data['vegetables']),
            ', '.join(order_data['fruits']),
            ', '.join(order_data['meats']),
            order_data['quantity']
        ))
        
        conn.commit()
        print(f"Data inserted successfully: {order_data}")
        cursor.close()
        conn.close()
    except mysql.connector.Error as err:
        print(f"Database error: {err}")
        return False
    except Exception as e:
        print(f"Unexpected error: {e}")
        return False
    return True

# Function to send the order email
def send_order_email(customer_email, order_details):
    sender_email = os.getenv("SENDER_EMAIL","tejakumar2121@gmail.com")
    sender_password = os.getenv("SENDER_PASSWORD","ifmwbxgycvsaqwbv")

    message = MIMEMultipart()
    message["From"] = sender_email
    message["To"] = customer_email
    message["Subject"] = "Your Order Details"

    body = f"Thank you for your order. Here are your details:\n\n{order_details}"
    message.attach(MIMEText(body, "plain"))

    try:
        with smtplib.SMTP("smtp.gmail.com", 587) as server:
            server.starttls()
            server.login(sender_email, sender_password)
            server.send_message(message)
            print("Email sent successfully.")
    except Exception as e:
        print(f"Error sending email: {e}")

# Route to render the HTML form
@app.route('/')
def order_form():
    return render_template('main.html')

# Route to handle form submission
@app.route('/submit-order', methods=['POST'])
def submit_order():
    name = request.form['customer-name']
    email = request.form['customer-email']
    phone = request.form['customer-phone']
    vegetable = request.form['item-select-vegetable']
    fruit = request.form['item-select-fruit']
    meat = request.form['item-select-meat']
    quantity = request.form['quantity']

    # Format the order details for the email
    order_details = f"""
    Name: {name}
    Email: {email}
    Phone: {phone}
    Vegetable: {vegetable}
    Fruit: {fruit}
    Meat: {meat}
    Quantity: {quantity}
    """
    print( order_details)

    # Send the order email
    send_order_email(email, order_details)


    return redirect(url_for('order_confirmation', name=name))

# Route to display the order confirmation page
@app.route('/confirmation-details')
def order_confirmation():
    name = request.args.get('name')

    return f"<h1>Thank you, {name}! Your order has been placed successfully.</h1>"

if __name__ == '__main__':
    app.run(debug=True)







