from flask import Flask, request, jsonify, session, render_template, redirect, url_for
from flask_cors import CORS
from werkzeug.security import generate_password_hash, check_password_hash
import datafetch

app = Flask(__name__)
app.secret_key = "dayflow-change-this-secret-key"
CORS(app, supports_credentials=True)

# ---------- PAGE ROUTES ----------
@app.route("/")
@app.route("/login")
def login_page(): return render_template("login.html")

@app.route("/home")
def employee_home():
    if "employee_id" not in session: return redirect(url_for("login_page"))
    return redirect(url_for("hr_home")) if session.get("role") == "hr" else render_template("homepage.html")

@app.route("/hr")
def hr_home():
    if session.get("role") != "hr": return redirect(url_for("login_page"))
    return render_template("hr_home.html")

@app.route("/profile")
def profile_page():
    if "employee_id" not in session: return redirect(url_for("login_page"))
    return render_template("profile.html")

@app.route("/attendance")
def attendance_page():
    if "employee_id" not in session: return redirect(url_for("login_page"))
    return render_template("attendence.html")

@app.route("/leave")
def leave_page():
    if "employee_id" not in session: return redirect(url_for("login_page"))
    return render_template("leave.html")

@app.route("/payroll")
def payroll_page():
    if "employee_id" not in session: return redirect(url_for("login_page"))
    return render_template("payroll.html")

@app.route("/employees")
def employees_page():
    if session.get("role") != "hr": return redirect(url_for("login_page"))
    return render_template("employees.html")

@app.route("/attendance-management")
def attendance_management_page():
    if session.get("role") != "hr": return redirect(url_for("login_page"))
    return render_template("attendance_management.html")

@app.route("/leave-approvals")
def leave_approvals_page():
    if session.get("role") != "hr": return redirect(url_for("login_page"))
    return render_template("leave_approvals.html")

@app.route("/payroll-management")
def payroll_management_page():
    if session.get("role") != "hr": return redirect(url_for("login_page"))
    return render_template("payroll_management.html")

# ---------- AUTH ----------
@app.route("/api/signup", methods=["POST"])
def signup():
    data = request.get_json(silent=True) or {}
    employee_id = str(data.get("employee_id", "")).strip()
    email = str(data.get("email", "")).strip().lower()
    password = data.get("password", "")
    role = str(data.get("role", "")).strip().lower()
    if not employee_id or not email or not password or not role:
        return jsonify(success=False, message="All fields are required."), 400
    if role not in ("employee", "hr"):
        return jsonify(success=False, message="Invalid role."), 400
    if len(password) < 8:
        return jsonify(success=False, message="Password must contain at least 8 characters."), 400
    try:
        datafetch.create_user(employee_id, email, generate_password_hash(password), role)
        datafetch.create_basic_profile(employee_id, employee_id)
        return jsonify(success=True, message="Account created successfully."), 201
    except Exception as exc:
        msg = str(exc)
        if "Duplicate" in msg or "duplicate" in msg: msg = "Employee ID or email is already registered."
        return jsonify(success=False, message=msg), 409

<<<<<<< HEAD
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
=======
@app.route("/api/login", methods=["POST"])
def login():
    data = request.get_json(silent=True) or {}
    email = str(data.get("email", data.get("Email", ""))).strip().lower()
    password = data.get("password", "")
    if not email or not password: return jsonify(success=False, status="error", message="Email and password are required."), 400
    user = datafetch.verify_login(email)
    if not user or not check_password_hash(user["password_hash"], password):
        return jsonify(success=False, status="error", message="Invalid email or password."), 401
    role = str(user["UserRole"]).lower()
    session["employee_id"], session["role"] = user["Employee_ID"], role
    user_response = {"employee_id": user["Employee_ID"], "email": user["Email"], "role": role}
    redirect_url = "/hr" if role == "hr" else "/home"
    return jsonify(success=True, status="success", message="Login successful.", user=user_response, data=user_response, redirect_url=redirect_url), 200

@app.route("/api/logout", methods=["POST", "GET"])
def logout():
    session.clear(); return jsonify(success=True, message="Logged out successfully.")

# ---------- PROFILE / EMPLOYEES ----------
@app.route("/api/profile/<employee_id>", methods=["GET"])
def get_profile(employee_id):
    row = datafetch.get_employee_profile(employee_id)
    return jsonify(success=bool(row), data=row) if row else (jsonify(success=False, message="Profile not found."), 404)

@app.route("/api/profile/<employee_id>", methods=["PUT"])
def update_profile(employee_id):
    data = request.get_json(silent=True) or {}
    fields = {"Name": data.get("name"), "Phone_no": data.get("phone"), "Address": data.get("address"), "Profile_pic_url": data.get("profile_pic_url")}
    fields = {k:v for k,v in fields.items() if v is not None}
    if not fields: return jsonify(success=False, message="No profile fields supplied."), 400
    try: datafetch.update_employee_profile(employee_id, fields); return jsonify(success=True, message="Profile updated successfully.")
    except Exception as exc: return jsonify(success=False, message=str(exc)), 400

@app.route("/api/employees", methods=["GET"])
def get_employees(): return jsonify(success=True, data=datafetch.get_all_employees())

@app.route("/api/employees", methods=["POST"])
def add_employee():
    data = request.get_json(silent=True) or {}
    try:
        datafetch.create_employee(data["employee_id"], data["email"], data["name"], data.get("phone"), data.get("address"), data.get("department"), data.get("designation"), data.get("manager_id"), data.get("doj"))
        return jsonify(success=True, message="Employee created successfully."), 201
    except KeyError: return jsonify(success=False, message="Employee ID, name and email are required."), 400
    except Exception as exc: return jsonify(success=False, message=str(exc)), 400

@app.route("/api/employees/<employee_id>", methods=["PUT"])
def edit_employee(employee_id):
    data = request.get_json(silent=True) or {}
    fields = {"Name":data.get("name"),"Phone_no":data.get("phone"),"Address":data.get("address"),"Department":data.get("department"),"Designation":data.get("designation"),"Manager_id":data.get("manager_id"),"DOJ":data.get("doj"),"Profile_pic_url":data.get("profile_pic_url"),"Doc_Links":data.get("doc_links")}
    fields = {k:v for k,v in fields.items() if v is not None}
    if not fields: return jsonify(success=False, message="No employee fields supplied."), 400
    try: datafetch.update_employee_profile(employee_id, fields); return jsonify(success=True, message="Employee updated successfully.")
    except Exception as exc: return jsonify(success=False, message=str(exc)), 400

# ---------- ATTENDANCE ----------
@app.route("/api/attendance/<employee_id>", methods=["GET"])
def get_attendance(employee_id): return jsonify(success=True, data=datafetch.get_employee_attendance(employee_id))

@app.route("/api/attendance/<employee_id>/check-in", methods=["POST"])
def check_in(employee_id):
    try: return jsonify(success=True, message="Check-in recorded.", data=datafetch.check_in_employee(employee_id)), 201
    except Exception as exc: return jsonify(success=False, message=str(exc)), 400

@app.route("/api/attendance/<employee_id>/check-out", methods=["POST"])
def check_out(employee_id):
    try: return jsonify(success=True, message="Check-out recorded.", data=datafetch.check_out_employee(employee_id))
    except Exception as exc: return jsonify(success=False, message=str(exc)), 400

@app.route("/api/admin/attendance/today", methods=["GET"])
def get_global_attendance(): return jsonify(success=True, data=datafetch.get_todays_global_attendance())

@app.route("/api/admin/attendance", methods=["GET"])
def get_admin_attendance(): return jsonify(success=True, data=datafetch.get_all_attendance())

# ---------- LEAVE ----------
@app.route("/api/leave/history/<employee_id>", methods=["GET"])
def get_leave_history(employee_id): return jsonify(success=True, data=datafetch.get_employee_leave_history(employee_id))

@app.route("/api/leave", methods=["POST"])
def apply_leave():
    data = request.get_json(silent=True) or {}
    try:
        leave_id = datafetch.create_leave_request(data["employee_id"], data["leave_type"], data["start_date"], data["end_date"], data.get("remarks", ""))
        return jsonify(success=True, message="Leave request submitted.", leave_id=leave_id), 201
    except KeyError: return jsonify(success=False, message="Employee, leave type and dates are required."), 400
    except Exception as exc: return jsonify(success=False, message=str(exc)), 400

@app.route("/api/admin/leave", methods=["GET"])
def get_all_leave_requests(): return jsonify(success=True, data=datafetch.get_all_leave_requests())

@app.route("/api/admin/leave/pending", methods=["GET"])
def get_pending_leaves(): return jsonify(success=True, data=datafetch.get_pending_leave_approvals())

@app.route("/api/admin/leave/<int:leave_id>/<action>", methods=["POST"])
def leave_action(leave_id, action):
    if action not in ("approve", "reject"): return jsonify(success=False, message="Invalid action."), 400
    data = request.get_json(silent=True) or {}
    try:
        datafetch.update_leave_status(leave_id, "Approved" if action == "approve" else "Rejected", data.get("comments", ""), data.get("approver_id"))
        return jsonify(success=True, message=f"Leave request {action}d successfully.")
    except Exception as exc: return jsonify(success=False, message=str(exc)), 400

# ---------- PAYROLL ----------
@app.route("/api/payroll/<employee_id>", methods=["GET"])
def get_employee_payroll(employee_id): return jsonify(success=True, data=datafetch.get_employee_payroll(employee_id))

@app.route("/api/admin/payroll", methods=["GET"])
def get_all_payroll(): return jsonify(success=True, data=datafetch.get_all_payroll())

@app.route("/api/admin/payroll/<employee_id>", methods=["POST", "PUT"])
def save_payroll(employee_id):
    data = request.get_json(silent=True) or {}
    try:
        pid = datafetch.upsert_payroll(employee_id, data.get("base_salary",0), data.get("allowances",0), data.get("deductions",0), data.get("pay_period"))
        return jsonify(success=True, message="Payroll saved successfully.", payroll_id=pid)
    except Exception as exc: return jsonify(success=False, message=str(exc)), 400

# ---------- DASHBOARD ----------
@app.route("/api/admin/dashboard", methods=["GET"])
def admin_dashboard_metrics(): return jsonify(success=True, data=datafetch.get_dashboard_metrics())

if __name__ == "__main__": app.run(debug=True, port=5000)
>>>>>>> 096b2c8c6915e2ec7be07a72c9b0e2bd4a2e3890
