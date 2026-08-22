from flask import Flask, request, jsonify
from flask_cors import CORS
import sqlfunc
import datafetch

app = Flask(__name__)
CORS(app)  # Enables frontend-to-backend communication

# Database credentials
host = 'localhost'
user = 'root'
password = 'Hussain13620_root' # replace with your password if needed
database = 'dayflow_hrms'

# ==========================================
# 1. AUTHENTICATION (Login)
# ==========================================
@app.route('/api/login', methods=['POST'])
def login():
    data = request.json
    email = data.get('Email')
    
    user_data = datafetch.verify_login(email)
    
    if user_data:
        return jsonify({"status": "success", "data": user_data}), 200
    else:
        return jsonify({"status": "error", "message": "User not found"}), 404

# ==========================================
# 2. EMPLOYEE PROFILES
# ==========================================
@app.route('/api/profile/<employee_id>', methods=['GET'])
def get_profile(employee_id):
    profile = datafetch.get_employee_profile(employee_id)
    if profile:
        return jsonify({"status": "success", "data": profile}), 200
    return jsonify({"status": "error", "message": "Profile not found"}), 404

# ==========================================
# 3. ATTENDANCE MANAGEMENT
# ==========================================
@app.route('/api/attendance/<employee_id>', methods=['GET'])
def get_attendance(employee_id):
    history = datafetch.get_employee_attendance(employee_id)
    return jsonify({"status": "success", "data": history}), 200

@app.route('/api/admin/attendance/today', methods=['GET'])
def get_global_attendance():
    global_attendance = datafetch.get_todays_global_attendance()
    return jsonify({"status": "success", "data": global_attendance}), 200

# ==========================================
# 4. LEAVE MANAGEMENT
# ==========================================
@app.route('/api/leave/history/<employee_id>', methods=['GET'])
def get_leave_history(employee_id):
    history = datafetch.get_employee_leave_history(employee_id)
    return jsonify({"status": "success", "data": history}), 200

@app.route('/api/admin/leave/pending', methods=['GET'])
def get_pending_leaves():
    pending = datafetch.get_pending_leave_approvals()
    return jsonify({"status": "success", "data": pending}), 200

# ==========================================
# 5. ADMIN DASHBOARD METRICS
# ==========================================
@app.route('/api/admin/dashboard', methods=['GET'])
def admin_dashboard_metrics():
    headcount = datafetch.get_total_employee_count()
    on_leave = datafetch.get_active_on_leave_count()
    
    return jsonify({
        "status": "success",
        "data": {
            "total_employees": headcount['total_employees'] if headcount else 0,
            "on_leave_today": on_leave['on_leave_today'] if on_leave else 0
        }
    }), 200

# ==========================================
# 6. UNIVERSAL DATA INSERTION
# ==========================================
@app.route('/api/insert/<table_name>', methods=['POST'])
def insert_data(table_name):
    data = request.json
    try:
        sqlfunc.insertdata(host, user, password, database, table_name, data)
        return jsonify({"status": "success", "message": f"Successfully inserted into {table_name}"}), 201
    except Exception as e:
        return jsonify({"status": "error", "message": str(e)}), 400

# ==========================================
# START THE SERVER
# ==========================================
if __name__ == '__main__':
    app.run(debug=True, port=5000)
    # ==========================================
# 7. ADMIN DIRECTORY & PAYROLL ROUTES
# ==========================================
@app.route('/api/admin/employees', methods=['GET'])
def admin_get_employees():
    employees = datafetch.get_all_employees()
    return jsonify({"status": "success", "data": employees}), 200

@app.route('/api/admin/payroll', methods=['GET'])
def admin_get_payroll():
    payroll_records = datafetch.get_all_payroll()
    return jsonify({"status": "success", "data": payroll_records}), 200