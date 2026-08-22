import mysql.connector
def get_db_connection(_host,_user,_password,_database):
    connection=mysql.connector.connect(host=_host,user=_user,password=_password,database=_database)
    return connection 
def createtable(_host,_user,_password,_database,table_name:str,table_structure:dict):
    connection=get_db_connection(_host,_user,_password,_database)
    cursor=connection.cursor()
    column_def=[]
    for col_name,data_type in table_structure.items():
        column_def.append(f"{col_name} {data_type}")
        columns_str=','.join(column_def)
    query=f"CREATE TABLE IF NOT EXISTS {table_name} ({columns_str}) "
    cursor.execute(query)
    cursor.close()
    connection.close()
    print(f"The table {table_name} has been created in database {_database}")
def insertdata(_host,_user,_password,_database,table_name:str,data:dict):
    connection=get_db_connection(_host,_user,_password,_database)
    cursor=connection.cursor()
    columns=",".join(data.keys())
    values=tuple(data.values())
    place_holders=",".join(["%s"]*len(data))
    query=f"INSERT INTO {table_name} ({columns}) VALUES ({place_holders})"
    cursor.execute(query,values)
    connection.commit()
    print(f"Data has been inserted into the table {table_name}")
    cursor.close()
    connection.close()
def displayall(_host,_user,_password,_database,table_name:str):
    connection=get_db_connection(_host,_user,_password,_database)
    cursor=connection.cursor()
    query=f"SELECT * FROM {table_name}"
    cursor.execute(query)
    data=cursor.fetchall()
    for row in data:
        print(row)
    cursor.close()
    connection.close()
def createdict():
    dictn={}
    no_of_elements=int(input("Enter the no. of elements you want in a dictionary: "))
    for i in range(0,no_of_elements):
        key=input("Enter key:")
        valchoice=int(input("Which data type of value do you want to enter? \n1:string\n2:integer\n3:float:"))
        value=input("Enter value:")
        if valchoice==2:
            value=int(value)
        if valchoice==3:
            value=float(value)
        dictn[key]=value
        print("element inserted into the dictionary")
    return dictn
