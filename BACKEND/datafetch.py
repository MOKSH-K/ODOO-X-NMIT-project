import sqlfunc

# Database credentials
host = 'localhost'
user = 'root'
password = 'Hussain13620_root' #replace with your password
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
    
    query = "SELECT Employee_ID, password_hash, UserRole FROM UserAndAuth WHERE Email = %s"
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
    
    query = "SELECT * FROM EMPprof WHERE Employee_ID = %s"
    cursor.execute(query, (employee_id,))
    profile_data = cursor.fetchone()
    
    cursor.close()
    connection.close()
    return profile_data


# ==========================================
# 3. ATTENDANCE MANAGEMENT
# ==========================================

# Grabs the punch-in/punch-out history for a specific person
def get_employee_attendance(employee_id):
    connection = sqlfunc.get_db_connection(host, user, password, database)
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT Log_Date, Check_In_Time, Check_Out_Time, Status 
        FROM Attendance 
        WHERE Employee_ID = %s 
        ORDER BY Log_Date DESC
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
        SELECT e.Name, a.Log_Date, a.Check_In_Time, a.Check_Out_Time, a.Status 
        FROM Attendance a 
        JOIN EMPprof e ON a.Employee_ID = e.Employee_ID 
        WHERE a.Log_Date = CURDATE()
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
        SELECT Leave_ID, Leave_Type, Start_Date, End_Date, Status, Remarks 
        FROM LeaveRequests 
        WHERE Employee_ID = %s 
    """
    cursor.execute(query, (employee_id,))
    leave_history = cursor.fetchall()
    
    cursor.close()
    connection.close()
    return leave_history


'''Another bridge (JOIN). HR needs an inbox of vacation requests to approve or deny.
   This grabs only the leaves marked as 'Pending' and attaches the employee's real name
   so HR knows who is asking for time off'''

def get_pending_leave_approvals():
    """ADMIN VIEW: Fetches all pending leaves and attaches the employee's name."""
    connection = sqlfunc.get_db_connection(host, user, password, database)
    cursor = connection.cursor(dictionary=True)
    
    query = """
        SELECT l.Leave_ID, e.Name, e.Employee_ID, l.Leave_Type, l.Start_Date, l.End_Date, l.Remarks 
        FROM LeaveRequests l 
        JOIN EMPprof e ON l.Employee_ID = e.Employee_ID 
        WHERE l.Status = 'Pending'
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
    
    query = "SELECT COUNT(*) AS total_employees FROM EMPprof"
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
        FROM LeaveRequests 
        WHERE Status = 'Approved' AND CURDATE() BETWEEN Start_Date AND End_Date
    """
    cursor.execute(query)
    total_on_leave = cursor.fetchone()
    
    cursor.close()
    connection.close()
    return total_on_leave
# ==========================================
# ADMIN: GET ALL EMPLOYEES & PROFILES
# ==========================================
def get_all_employees():
    connection = sqlfunc.get_db_connection()
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
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error fetching employees: {e}")
        return []
    finally:
        cursor.close()
        connection.close()

# ==========================================
# ADMIN: GET ALL PAYROLL RECORDS
# ==========================================
def get_all_payroll():
    connection = sqlfunc.get_db_connection()
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
        result = cursor.fetchall()
        return result
    except Exception as e:
        print(f"Error fetching payroll: {e}")
        return []
    finally:
        cursor.close()
        connection.close()