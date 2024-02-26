import pyodbc
import pandas as pd


class AzureSqlDbConnection:
 
 def __init__(self, username="Enter here your azure database username", password="Enter here your azure database P@ssw0rd", server="Enter here your azure database server like 'zee.database.windows.net'", database="Enter here your azure database database name like 'zeestreampass'"):
    self.username = username
    self.password = password
    self.server = server
    self.database = database
    driver = '{ODBC Driver 17 for SQL Server}'
    port = 1433
    self.conn_str = f"DRIVER={driver};SERVER={server};DATABASE={database};UID={username};PWD={password};PORT={port};"
 def get_table_names(self):
    # Establish the connection
    conn = pyodbc.connect(self.conn_str)

    # Query for retrieving all table names
    query = "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_TYPE='BASE TABLE';"

    # Execute query and retrieve table names
    table_names = pd.read_sql(query, conn)['TABLE_NAME']
    # # Print number of tables
    # print(f'Number of tables: {len(table_names)}')
    # Close the connection
    conn.close()
    return table_names
 
 def insert_user(self, usernames, name, email, password, normalpass):
   
   conn = pyodbc.connect(self.conn_str)
   # Create a cursor from the connection
   cursor = conn.cursor()
   # Use ? placeholders for values and provide a tuple of values as the second argument to execute()
   cursor.execute("INSERT INTO [dbo].[user] (usernames, name, email, password, normalpass) VALUES (?, ?, ?, ?, ?)", (usernames, name, email, password, normalpass))
   conn.commit()

   # Close the connection
   conn.close()
   return "User added of success has been added."
 
def check_user_credentials(self, email, password):
    try:
        with pyodbc.connect(self.conn_str) as conn:
            cursor = conn.cursor()
            # Execute query to check if email and password match
            cursor.execute("SELECT usernames, name FROM [dbo].[user] WHERE usernames = ? AND normalpass = ?", (email, password))
            row = cursor.fetchone()
            if row:
                usernames, name = row
                return True, usernames, name
            else:
                return False, None, None
            # count = cursor.fetchone()[0]
            # return count > 0
    except pyodbc.Error as e:
        print("Error:", e)
        return False






# # Example usage
# if __name__ == "__main__":

#     username="Enter here your azure database username"
#     password="Enter here your azure database P@ssw0rd"
#     server="Enter here your azure database server like 'zee.database.windows.net"
#     database="Enter here your azure database database name like zeestreampass"
#     conn = AzureSqlDbConnection(username,password,server,database)
    
#     email = input("Enter your email: ")
#     password = input("Enter your password: ")
#     authenticated, username, name = conn.check_user_credentials(email, password)
#     if authenticated:
#         print("username : ", username)
#         print("name : ", name)
#         print("Login successful!")
#     else:
#         print("Invalid email or password.")