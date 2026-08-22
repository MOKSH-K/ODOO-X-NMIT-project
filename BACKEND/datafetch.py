import sqlfunc

# Database credentials
host = 'localhost'
user = 'root'
password = 'Hussain13620_root'#replace with your password
database = 'dayflow_hrms'

# ==========================================
# 1. AUTHENTICATION (Login)
# ==========================================


'''When a user tries to log in, they provide an email. This query goes into the users table,
   finds that exact email, and hands back the user's ID, their encrypted password (password_hash),
   and their role (Admin vs. Employee)'''

def verify_login(email):
    connection = sqlfunc.get_db_connection(host, user, password, database)
    cursor = connection.cursor(dictionary=True) 
    
    query = "SELECT employee_id, password_hash, role FROM users WHERE email = %s"
    cursor.execute(query, (email,))
    user_data = cursor.fetchone() 
    
    cursor.close()
    connection.close()
    return user_data


# ==========================================
# 2. EMPLOYEE PROFILES
# ==========================================


'''The * symbol means "select everything." It fetches every single column (name, department, role, etc.)
   for one specific employee. This is what populates the "My Profile" page on the frontend'''

def get_employee_profile(employee_id):
    connection = sqlfunc.get_db_connection(host, user, password, database)
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT * FROM employees WHERE employee_id = %s"
    cursor.execute(query, (employee_id,))
    profile_data = cursor.fetchone()
    
    cursor.close()
    connection.close()
    return profile_data


'''Instead of fetching everything, this only grabs the names of the documents and the links (file_path)
   to where those files are stored.
   The frontend uses these links to create clickable download buttons'''

def get_employee_documents(employee_id):
    connection = sqlfunc.get_db_connection(host, user, password, database)
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT document_title, file_path FROM employee_documents WHERE employee_id = %s"
    cursor.execute(query, (employee_id,))
    documents = cursor.fetchall() 
    
    cursor.close()
    connection.close()
    return documents


# ==========================================
# 3. ATTENDANCE MANAGEMENT
# ==========================================
# Grabs the punch-in/punch-out history for a specific person
def get_employee_attendance(employee_id):
    connection = sqlfunc.get_db_connection(host, user, password, database)
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT date, check_in_time, check_out_time, status 
        FROM attendance_records 
        WHERE employee_id = %s 
        ORDER BY date DESC
    """
    cursor.execute(query, (employee_id,))
    attendance_history = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return attendance_history


'''This is for the HR dashboard. The attendance table only stores the employee_id, which isn't helpful for a human reading it.
   The JOIN acts like a bridge, connecting the attendance record to the employees table
   so HR can see the actual full_name of everyone who clocked in'''

def get_todays_global_attendance():
    """ADMIN VIEW: Fetches today's attendance for all employees with their names."""
    connection = sqlfunc.get_db_connection(host, user, password, database)
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT e.full_name, a.date, a.check_in_time, a.check_out_time, a.status 
        FROM attendance_records a 
        JOIN employees e ON a.employee_id = e.employee_id 
        WHERE a.date = CURDATE()
    """
    cursor.execute(query)
    global_attendance = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return global_attendance


# ==========================================
# 4. LEAVE MANAGEMENT
# ==========================================

#Fetches all past and present vacation/sick leave requests for an employee, newest ones first

def get_employee_leave_history(employee_id):
    connection = sqlfunc.get_db_connection(host, user, password, database)
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT request_id, leave_type, start_date, end_date, duration_days, status, remarks 
        FROM leave_requests 
        WHERE employee_id = %s 
        ORDER BY created_at DESC
    """
    cursor.execute(query, (employee_id,))
    leave_history = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return leave_history


'''subtracts the used days from the total days
   and uses AS to create a brand new column named paid_remaining right in the final JSON'''

def get_employee_leave_balance(employee_id, year):
    """Calculates remaining leave balances by doing math directly in SQL."""
    connection = sqlfunc.get_db_connection(host, user, password, database)
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT 
            (paid_leave_total - paid_leave_used) AS paid_remaining, 
            (sick_leave_total - sick_leave_used) AS sick_remaining 
        FROM leave_balances 
        WHERE employee_id = %s AND year = %s
    """
    cursor.execute(query, (employee_id, year))
    balances = cursor.fetchone()
    
    cursor.close()
    connection.close()
    return balances


'''Another bridge (JOIN). HR needs an inbox of vacation requests to approve or deny.
   This grabs only the leaves marked as 'Pending' and attaches the employee's real name
   so HR knows who is asking for time off'''

def get_pending_leave_approvals():
    """ADMIN VIEW: Fetches all pending leaves and attaches the employee's name."""
    connection = sqlfunc.get_db_connection(host, user, password, database)
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT l.request_id, e.full_name, e.employee_id, l.leave_type, l.start_date, l.end_date, l.remarks 
        FROM leave_requests l 
        JOIN employees e ON l.employee_id = e.employee_id 
        WHERE l.status = 'Pending'
    """
    cursor.execute(query)
    pending_leaves = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return pending_leaves


# ==========================================
# 5. ADMIN DASHBOARD METRICS
# ==========================================


# counts the number of rows in the table. Instead of downloading all 500 employee profiles to count them

def get_total_employee_count():
    connection = sqlfunc.get_db_connection(host, user, password, database)
    cursor = connection.cursor(dictionary=True)
    
    query = "SELECT COUNT(*) AS total_employees FROM employees"
    cursor.execute(query)
    total = cursor.fetchone()
    
    cursor.close()
    connection.close()
    return total


'''This tells HR exactly who is out of the office right now. It checks two things: first,
   that HR actually approved the leave,and second,
   that today's exact date (CURDATE()) falls somewhere BETWEEN the employee's start and end dates'''

def get_active_on_leave_count():
    connection = sqlfunc.get_db_connection(host, user, password, database)
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT COUNT(*) AS on_leave_today 
        FROM leave_requests 
        WHERE status = 'Approved' AND CURDATE() BETWEEN start_date AND end_date
    """
    cursor.execute(query)
    total_on_leave = cursor.fetchone()
    
    cursor.close()
    connection.close()
    return total_on_leave