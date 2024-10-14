from flask import Flask, request, jsonify
from flask_cors import CORS
import mysql.connector
from mysql.connector import Error

app = Flask(__name__)
CORS(app)  # เพิ่ม CORS ให้กับ Flask

# การเชื่อมต่อกับฐานข้อมูล
def create_connection():
    connection = None
    try:
        connection = mysql.connector.connect(
            host='mydatabase.c30aq6k4gd00.us-east-1.rds.amazonaws.com',  # ใช้ endpoint ของ RDS
            user='admin',      # ใส่ชื่อผู้ใช้ของ RDS
            password='64160139',  # ใส่รหัสผ่านของ RDS
            database='mydatabase',  # ชื่อฐานข้อมูลใน RDS
            port=3306  # RDS ปกติจะใช้ port 3306 สำหรับ MySQL
        )
        print("MySQL connection successful")
    except Error as e:
        print(f"The error '{e}' occurred")
    return connection

# Route สำหรับรับข้อมูลจากฟอร์ม
@app.route('/register', methods=['POST'])
def register_student():
    data = request.json
    name = data['name']
    role = data['role']
    user_id = data['userId']
    
    connection = create_connection()
    
    if connection is None:
        return jsonify({"error": "Database connection failed."}), 500

    cursor = connection.cursor()

    try:
        sql = "INSERT INTO students (name, role, user_id) VALUES (%s, %s, %s)"
        val = (name, role, user_id)
        cursor.execute(sql, val)
        connection.commit()
    except Error as e:
        return jsonify({"error": "Unable to insert data."}), 500
    finally:
        cursor.close()
        connection.close()

    return jsonify({'name': name, 'role': role, 'userId': user_id})

# Route สำหรับดึงข้อมูลทั้งหมด
@app.route('/students', methods=['GET'])
def get_students():
    connection = create_connection()
    if connection is None:
        return jsonify({"error": "Database connection failed."}), 500

    cursor = connection.cursor(dictionary=True)
    cursor.execute("SELECT * FROM students;")
    students = cursor.fetchall()

    cursor.close()
    connection.close()
    
    return jsonify(students)

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)  # เปลี่ยนให้ฟังจากทุกที่
