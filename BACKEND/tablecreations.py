import mysql.connector
import sqlfunc
host='localhost'
user='root'
password='Hussain13620_root'#replace with your password
database='dayflow_hrms'
# 1. User and Authentication
table_name1='UserAndAuth'
schema1={"Employee_ID":"INT PRIMARY KEY",
"Email":"VARCHAR(100) UNIQUE NOT NULL",
"password_hash":"VARCHAR(255) NOT NULL",
"UserRole":"VARCHAR(255) DEFAULT 'Employee'",
"email_ver":"BOOLEAN DEFAULT FALSE"}
sqlfunc.createtable(host,user,password,database,table_name1,schema1)
# 2. Employee Profile
table_name2="EMPprof"
schema2={"Employee_ID":"INT",
         "Name":"VARCHAR(100) NOT NULL",
         "Phone_no":"INT",
         "Address":"TEXT",
         "Profile_pic_url":"VARCHAR(255)",
         "Department":"VARCHAR(50)",
         "Designation":"VARCHAR(50)",
         "Manager_id":"INT",
         "Doc_Links":"TEXT",
         "DOJ":"DATE"}
sqlfunc.createtable(host,user,password,database,table_name2,schema2)
# 3. Attendance Table
table_name3 = "Attendance"
schema3 = {
    "Attendance_ID": "INT AUTO_INCREMENT PRIMARY KEY",
    "Employee_ID": "INT",
    "Log_Date": "DATE",
    "Check_In_Time": "DATETIME",
    "Check_Out_Time": "DATETIME",
    "Status": "VARCHAR(20)",
    "FOREIGN KEY (Employee_ID)": "REFERENCES UserAndAuth(Employee_ID) ON DELETE CASCADE"
}
sqlfunc.createtable(host, user, password, database, table_name3, schema3)
# 4. Leave Requests Table
table_name4 = "LeaveRequests"
schema4 = {
    "Leave_ID": "INT AUTO_INCREMENT PRIMARY KEY",
    "Employee_ID": "INT",
    "Leave_Type": "VARCHAR(20)",
    "Start_Date": "DATE",
    "End_Date": "DATE",
    "Remarks": "TEXT",
    "Status": "VARCHAR(20) DEFAULT 'Pending'",
    "Admin_Comments": "TEXT",
    "Approver_ID": "INT",
    "FOREIGN KEY (Employee_ID)": "REFERENCES UserAndAuth(Employee_ID) ON DELETE CASCADE"
}
sqlfunc.createtable(host, user, password, database, table_name4, schema4)
# 5. Payroll Table
table_name5 = "Payroll"
schema5 = {
    "Payroll_ID": "INT AUTO_INCREMENT PRIMARY KEY",
    "Employee_ID": "INT",
    "Base_Salary": "DECIMAL(10, 2)",
    "Allowances": "DECIMAL(10, 2)",
    "Deductions": "DECIMAL(10, 2)",
    "Net_Pay": "DECIMAL(10, 2)",
    "Pay_Period": "DATE",
    "FOREIGN KEY (Employee_ID)": "REFERENCES UserAndAuth(Employee_ID) ON DELETE CASCADE"
}
sqlfunc.createtable(host, user, password, database, table_name5, schema5)

    