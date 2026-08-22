import sqlfunc

host = 'localhost'
user = 'root'
password = 'Hussain13620_root'
database = 'dayflow_hrms'

print("Seeding consistent test data...")

# 1. Create the Login User (Using 102 instead of EMP-102 because it is an INT)
sqlfunc.insertdata(host, user, password, database, "UserAndAuth", {
    "Employee_ID": 102,
    "Email": "alex.j@dayflow.com",
    "password_hash": "hashed_123",
    "UserRole": "Employee",
    "email_ver": True
})

# 2. Create their Profile in EMPprof 
# (Make sure you added Employee_ID to your EMPprof schema!)
sqlfunc.insertdata(host, user, password, database, "EMPprof", {
    "Employee_ID": 102,
    "Name": "Alex Johnson",
    "Phone_no": 1234567890,
    "Department": "Engineering",
    "Designation": "Backend Dev"
})

print("Database is consistently seeded and ready for the API!")