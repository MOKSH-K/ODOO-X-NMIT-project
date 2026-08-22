import mysql.connector

def insertdata(host, user, password, database, table_name, data_dict):
    """
    Universally inserts a dictionary of keys and values into any given MySQL table.
    """
    connection = None
    cursor = None
    try:
        connection = mysql.connector.connect(
            host=host,
            user=user,
            password=password,
            database=database
        )
        cursor = connection.cursor()

        # Extract column names and values from the incoming JSON dictionary
        columns = list(data_dict.keys())
        values = list(data_dict.values())

        # Construct the SQL INSERT statement dynamically
        cols_formatted = ", ".join(columns)
        placeholders = ", ".join(["%s"] * len(values))
        
        query = f"INSERT INTO {table_name} ({cols_formatted}) VALUES ({placeholders})"

        # Execute and commit
        cursor.execute(query, values)
        connection.commit()
        
        return True

    except Exception as e:
        if connection:
            connection.rollback()
        print(f"Error in sqlfunc insertdata: {e}")
        raise e

    finally:
        if cursor:
            cursor.close()
        if connection:
            connection.close()