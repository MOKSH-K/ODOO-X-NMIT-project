import mysql.connector

# Database credentials configuration (adjust if needed)
DB_CONFIG = {
    'host': 'localhost',
    'user': 'root',
    'password': 'Hussain13620_root',
    'database': 'dayflow_hrms'
}

def get_db_connection():
    try:
        connection = mysql.connector.connect(**DB_CONFIG)
        return connection
    except mysql.connector.Error as err:
        print(f"Database connection error: {err}")
        return None

# ==========================================
# 1. AUTHENTICATION
# ==========================================
def verify_login(email):
    connection = get_db_connection()
    if not connection:
        return None
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT Employee_ID, Email, UserRole FROM UserAndAuth WHERE Email = %s"
        cursor.execute(query, (email,))
        user = cursor.fetchone()
        return user
    except Exception as e:
        print(f"Error verifying login: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

# ==========================================
# 2. EMPLOYEE PROFILE
# ==========================================
def get_employee_profile(employee_id):
    connection = get_db_connection()
    if not connection:
        return None
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT p.Employee_ID, p.Name, p.Department, p.Designation, p.Phone_no, p.DOJ, u.Email 
            FROM EMPprof p
            LEFT JOIN UserAndAuth u ON p.Employee_ID = u.Employee_ID
            WHERE p.Employee_ID = %s
        """
        cursor.execute(query, (employee_id,))
        profile = cursor.fetchone()
        return profile
    except Exception as e:
        print(f"Error fetching profile: {e}")
        return None
    finally:
        cursor.close()
        connection.close()

# ==========================================
# 3. ATTENDANCE
# ==========================================
def get_employee_attendance(employee_id):
    connection = get_db_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT Log_Date, Check_In_Time, Check_Out_Time, Status FROM AttendanceLogs WHERE Employee_ID = %s ORDER BY Log_Date DESC"
        cursor.execute(query, (employee_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching attendance: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def get_todays_global_attendance():
    connection = get_db_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    try:
        # Fetches attendance for today joined with employee names
        query = """
            SELECT a.Employee_ID, p.Name, a.Check_In_Time, a.Check_Out_Time, a.Status, a.Log_Date
            FROM AttendanceLogs a
            LEFT JOIN EMPprof p ON a.Employee_ID = p.Employee_ID
            WHERE a.Log_Date = CURDATE()
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching global attendance: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

# ==========================================
# 4. LEAVE MANAGEMENT
# ==========================================
def get_employee_leave_history(employee_id):
    connection = get_db_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT Leave_Type, Start_Date, End_Date, Remarks, Status FROM LeaveRequests WHERE Employee_ID = %s"
        cursor.execute(query, (employee_id,))
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching leave history: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

def get_pending_leave_approvals():
    connection = get_db_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT l.Request_ID, l.Employee_ID, p.Name, l.Leave_Type, l.Start_Date, l.End_Date, l.Remarks, l.Status
            FROM LeaveRequests l
            LEFT JOIN EMPprof p ON l.Employee_ID = p.Employee_ID
            WHERE l.Status = 'Pending'
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching pending leaves: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

# ==========================================
# 5. ADMIN DASHBOARD METRICS
# ==========================================
def get_total_employee_count():
    connection = get_db_connection()
    if not connection:
        return {"total_employees": 0}
    cursor = connection.cursor(dictionary=True)
    try:
        cursor.execute("SELECT COUNT(*) AS total_employees FROM UserAndAuth")
        return cursor.fetchone()
    except Exception as e:
        print(f"Error counting employees: {e}")
        return {"total_employees": 0}
    finally:
        cursor.close()
        connection.close()

def get_active_on_leave_count():
    connection = get_db_connection()
    if not connection:
        return {"on_leave_today": 0}
    cursor = connection.cursor(dictionary=True)
    try:
        query = "SELECT COUNT(*) AS on_leave_today FROM LeaveRequests WHERE Status = 'Approved' AND CURDATE() BETWEEN Start_Date AND End_Date"
        cursor.execute(query)
        return cursor.fetchone()
    except Exception as e:
        print(f"Error counting active leaves: {e}")
        return {"on_leave_today": 0}
    finally:
        cursor.close()
        connection.close()

# ==========================================
# 6. ADMIN: GET ALL EMPLOYEES & PROFILES
# ==========================================
def get_all_employees():
    connection = get_db_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT u.Employee_ID, u.Email, u.UserRole, 
                   p.Name, p.Department, p.Designation, p.Phone_no 
            FROM UserAndAuth u
            LEFT JOIN EMPprof p ON u.Employee_ID = p.Employee_ID
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching employees: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

# ==========================================
# 7. ADMIN: GET ALL PAYROLL RECORDS
# ==========================================
def get_all_payroll():
    connection = get_db_connection()
    if not connection:
        return []
    cursor = connection.cursor(dictionary=True)
    try:
        query = """
            SELECT pay.Payroll_ID, pay.Employee_ID, pay.Base_Salary, 
                   pay.Allowances, pay.Deductions, pay.Net_Pay, pay.Pay_Period,
                   p.Name, p.Department 
            FROM Payroll pay
            LEFT JOIN EMPprof p ON pay.Employee_ID = p.Employee_ID
        """
        cursor.execute(query)
        return cursor.fetchall()
    except Exception as e:
        print(f"Error fetching payroll: {e}")
        return []
    finally:
        cursor.close()
        connection.close()