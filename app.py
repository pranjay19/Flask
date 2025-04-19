from flask import Flask, request, jsonify
import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# MySQL DB connection
db = mysql.connector.connect(
    host=os.getenv("DB_HOST"),
    user=os.getenv("DB_USER"),
    password=os.getenv("DB_PASSWORD"),
    database=os.getenv("DB_NAME")
)
cursor = db.cursor()

# ------------------------------
# GET API to fetch all customers
# ------------------------------
@app.route('/customers', methods=['GET'])
def get_customers():
    cursor.execute("SELECT * FROM customers")
    rows = cursor.fetchall()

    results = []
    for row in rows:
        results.append({
            "id": row[0],
            "name": row[1],
            "email": row[2],
            "phone": row[3]
        })

    return jsonify(results), 200


# ------------------------------
# POST API to add a new customer
# ------------------------------
@app.route('/customers', methods=['POST'])
def add_customer():
    data = request.get_json()
    name = data['name']
    email = data['email']
    phone = data['phone']

    # Check if the email already exists
    check_query = "SELECT * FROM customers WHERE email = %s"
    cursor.execute(check_query, (email,))
    existing_customer = cursor.fetchone()

    if existing_customer:
        return jsonify({"message": "Customer with this email already exists"}), 409

    # Insert the new customer
    insert_query = "INSERT INTO customers (name, email, phone) VALUES (%s, %s, %s)"
    cursor.execute(insert_query, (name, email, phone))
    db.commit()

    return jsonify({"message": "Customer added successfully"}), 201

# Run the app
if __name__ == '__main__':
    app.run(debug=True)