import mysql.connector

def create_tables():
    try:
        connection = mysql.connector.connect(
            host='localhost',
            user='root',
            password='Hussain13620_root',
            database='dayflow_hrms'
        )
        cursor = connection.cursor()

        # 1. User Authentication Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS UserAndAuth (
                Employee_ID INT PRIMARY KEY,
                Email VARCHAR(100) UNIQUE NOT NULL,
                UserRole VARCHAR(50) NOT NULL,
                password_hash VARCHAR(255) NOT NULL,
                email_ver BOOLEAN DEFAULT FALSE
            )
        """)

        # 2. Employee Profile Table (Manager_ID and Document_Links removed)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS EMPprof (
                Employee_ID INT PRIMARY KEY,
                Name VARCHAR(100) NOT NULL,
                Department VARCHAR(100),
                Designation VARCHAR(100),
                Phone_no BIGINT,
                DOJ DATE,
                FOREIGN KEY (Employee_ID) REFERENCES UserAndAuth(Employee_ID) ON DELETE CASCADE
            )
        """)

        # 3. Attendance Logs Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS AttendanceLogs (
                Log_ID INT AUTO_INCREMENT PRIMARY KEY,
                Employee_ID INT,
                Log_Date DATE NOT NULL,
                Check_In_Time TIME,
                Check_Out_Time TIME,
                Status VARCHAR(50) NOT NULL,
                FOREIGN KEY (Employee_ID) REFERENCES UserAndAuth(Employee_ID) ON DELETE CASCADE
            )
        """)

        # 4. Leave Requests Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS LeaveRequests (
                Request_ID INT AUTO_INCREMENT PRIMARY KEY,
                Employee_ID INT,
                Leave_Type VARCHAR(50) NOT NULL,
                Start_Date DATE NOT NULL,
                End_Date DATE NOT NULL,
                Remarks TEXT,
                Status VARCHAR(50) DEFAULT 'Pending',
                FOREIGN KEY (Employee_ID) REFERENCES UserAndAuth(Employee_ID) ON DELETE CASCADE
            )
        """)

        # 5. Payroll Table
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS Payroll (
                Payroll_ID INT AUTO_INCREMENT PRIMARY KEY,
                Employee_ID INT,
                Base_Salary DECIMAL(10, 2) NOT NULL,
                Allowances DECIMAL(10, 2) DEFAULT 0.00,
                Deductions DECIMAL(10, 2) DEFAULT 0.00,
                Net_Pay DECIMAL(10, 2) NOT NULL,
                Pay_Period VARCHAR(50) NOT NULL,
                FOREIGN KEY (Employee_ID) REFERENCES UserAndAuth(Employee_ID) ON DELETE CASCADE
            )
        """)

        connection.commit()
        print("All database tables created successfully!")

    except Exception as e:
        print(f"Error creating tables: {e}")
    finally:
        if 'cursor' in locals() and cursor:
            cursor.close()
        if 'connection' in locals() and connection.is_connected():
            connection.close()

if __name__ == '__main__':
    create_tables()