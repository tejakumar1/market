
from flask import Flask, request, render_template, jsonify
import mysql.connector
import os
from dotenv import load_dotenv
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, request, render_template, redirect, url_for , request,session
load_dotenv()



app = Flask(__name__)
app.config['JSONIFY_PRETTYPRINT_REGULAR'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy()
def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydatabase.db'
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    # Bind SQLAlchemy to the app
    db.init_app(app)

    # Return the Flask app
    return app
app = create_app()
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)


@app.route('/')
def home():
    return "Database setup complete!"


# Database configuration
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': '',
    'database': 'market'
}

@app.route('/')
def main():
    return render_template('main.html')

@app.route('/view_cart')
def view_cart():
    return render_template('cart.html')
    

app = Flask(__name__)
app.secret_key = 'your_secret_key'

@app.route('/add-to-cart', methods=['POST'])
def add_to_cart():
    if 'cart' not in session:
        session['cart'] = []

    data = request.get_json()
    item = data.get('item')
    price = data.get('price')

    if item and price:
        session['cart'].append({'item': item, 'price': price})
        session.modified = True
        return jsonify({'success': True, 'cart': session['cart']})
    else:
        return jsonify({'success': False, 'error': 'Invalid data'})

    
@app.route('/cart', methods=['GET'])
def view_cart():
    cart = session.get('cart', [])
    return jsonify(cart)

# Function to insert order data into the database
def insert_order_data(order_data):
    try:
        conn = mysql.connector.connect(**db_config)
        cursor = conn.cursor()

        query = """
        INSERT INTO order (name, email, phone, vegetables, fruits, meats, location,comments)
        VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """
        cursor.execute(query, (
            order_data['name'],
            order_data['email'],
            order_data['phone'],
            ', '.join(order_data['vegetables']),
            ', '.join(order_data['fruits']),
            ', '.join(order_data['meats']),
            ', '.join(order_data['location']),
            ', '.join(order_data['comments'])

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
    location = request.form['location']
    comments = request.form['comments']

    # Format the order details for the email
    order_details = f"""
    Name: {name}
    Email: {email}
    Phone: {phone}
    Vegetable: {vegetable}
    Fruit: {fruit}
    Meat: {meat}
    location: {location}
    comments: {comments}
    """
    print( order_details)

    # Send the order email
    send_order_email(email, order_details)


    return redirect(url_for('order_confirmation', name=name))

# Route to display the order confirmation page
@app.route('/confirmation-details')
def order_confirmation():
    name = request.args.get('name')
    return f"""
        <style>
            @keyframes tick {{
                0% {{ transform: scale(0) rotate(45deg); }}
                50% {{ transform: scale(1.2) rotate(45deg); }}
                100% {{ transform: scale(1) rotate(45deg); }}
            }}
            @keyframes stroke {{
                100% {{ stroke-dashoffset: 0; }}
            }}
            @keyframes scale {{
                0%, 100% {{ transform: none; }}
                50% {{ transform: scale3d(1.1, 1.1, 1); }}
            }}
            body {{
                font-family: 'Poppins', sans-serif;
                color: #333;
                line-height: 1.6;
                text-align: center;
                margin: 0;
                padding: 0;
                background: linear-gradient(135deg, #00C851, #00A0FF);
                height: 100vh;
                display: flex;
                flex-direction: column;
                justify-content: center;
                align-items: center;
            }}
            h1 {{
                color: #0019;
                font-size: 2.5em;
                margin-bottom: 0.5em;
                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
            }}
            h1 span {{
                color: #FF5739; /* Vibrant orange color for the name */
                text-shadow: 2px 2px 5px rgba(0, 0, 0, 0.3);
            }}
            p {{
                background: rgba(255, 255, 255, 0.9);
                border: 1px solid #ddd;
                padding: 15px;
                border-radius: 10px;
                margin: 10px;
                font-size: 1.2em;
                color: #325;
            }}
            i {{
                color: #777;
            }}
            .checkmark {{
                width: 80px;
                height: 80px;
                display: block;
                stroke-width: 5;
                stroke: #00C851; /* Green color for tick mark */
                stroke-miterlimit: 10;
                margin: 20px auto;
            }}
            .checkmark__circle {{
                stroke-dasharray: 166;
                stroke-dashoffset: 166;
                stroke-width: 5;
                stroke-miterlimit: 10;
                stroke: #00C851; /* Green circle */
                fill: none;
                animation: stroke 1s cubic-bezier(.65, .05, .36, 1) forwards;
            }}
            .checkmark__check {{
                transform-origin: 50% 50%;
                stroke-dasharray: 48;
                stroke-dashoffset: 48;
                animation: stroke .5s cubic-bezier(.65, .05, .36, 1) .7s forwards;
            }}
            .content {{
                text-align: center;
                max-width: 600px;
                background: rgba(255, 255, 255, 0.8);
                padding: 20px;
                border-radius: 15px;
                box-shadow: 0px 4px 10px rgba(0, 0, 0, 0.2);
            }}
        </style>
        <body>
            <div class="content">
                <h1>Thank you, <span>{name}</span>!</h1>
                <svg class="checkmark" xmlns="http://www.w3.org/2000/svg" viewBox="0 0 52 52">
                    <circle class="checkmark__circle" cx="26" cy="26" r="25" fill="none"/>
                    <path class="checkmark__check" fill="none" d="M14 27l7 7 16-16"/>
                </svg>
                <p>Your order has been placed successfully.</p>
                <p>If you received a confirmation email, your order is confirmed.</p>
                <p><i>If you haven't received the email, please enter a valid email address.</i></p>
                <p>We will notify you when your order is shipped.</p>
            </div>
        </body>
    """

    


if __name__ == '__main__':
    app.run(debug=True)







