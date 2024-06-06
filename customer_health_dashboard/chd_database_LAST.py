import sqlite3
from flask import Flask, jsonify

app = Flask(__name__)

# Function to connect to SQLite3 database
def get_db_connection():
    conn = sqlite3.connect('data_generation/cs_health_dashboard.db')
    conn.row_factory = sqlite3.Row
    return conn

# Route to fetch customer data for the dashboard
@app.route('/dashboard', methods=['GET'])
def customer_success_dashboard():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM customers')
    customers = cursor.fetchall()
    conn.close()
    
    # Process and format data for the dashboard
    dashboard_data = process_customers_data(customers)
    
    return jsonify(dashboard_data)

def process_customers_data(customers):
    # Your logic to process customer data for the dashboard
    return [{"customer_id": row["id"], "health": row["health"]} for row in customers]

# if __name__ == '__main__':
#     app.run(debug=True)
