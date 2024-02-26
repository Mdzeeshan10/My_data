import pyodbc

conn = pyodbc.connect('DRIVER={ODBC Driver 17 for SQL Server};SERVER=stream-data.database.windows.net;DATABASE=stream-data-db;UID=zee;PWD=P@ssw0rd')


cursor = conn.cursor()

print("connect")

connn = 'DRIVER={ODBC Driver 17 for SQL Server};SERVER=stream-data.database.windows.net;DATABASE=stream-data-db;UID=zee;PWD=P@ssw0rd;PORT=1433;'


def check_user_credentials(email, password):
    try:
        with pyodbc.connect(connn) as conn:
            cursor = conn.cursor()
            # Execute query to check if email and password match
            cursor.execute("SELECT usernames, name FROM [dbo].[credentials] WHERE usernames = ? AND normalpass = ?", (email, password))
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
    

# Example usage
if __name__ == "__main__":
    email = input("Enter your email: ")
    password = input("Enter your password: ")
    authenticated, username, name = check_user_credentials(email, password)
    if authenticated:
        print("username : ", username)
        print("name : ", name)
        print("Login successful!")
    else:
        print("Invalid email or password.")
    print("----------------------1-----------------")

#     email = input("Enter your email: ")
#     password = input("Enter your password: ")
#     authenticated, username, name = check_user_credentials(email, password)
#     if authenticated:
#         print("username : ", username)
#         print("name : ", name)
#         print("Login successful!")
#     else:
#         print("Invalid email or password.")

#     print("----------------------2-----------------")

#     email = input("Enter your email: ")
#     password = input("Enter your password: ")
#     authenticated, username, name = check_user_credentials(email, password)
#     if authenticated:
#         print("username : ", username)
#         print("name : ", name)
#         print("Login successful!")
#     else:
#         print("Invalid email or password.")
    

# def insert_user(usernames, name, email, password, normalpass):
   
#    conn = pyodbc.connect(connn)
#    # Create a cursor from the connection
#    cursor = conn.cursor()
#    # Use ? placeholders for values and provide a tuple of values as the second argument to execute()
#    cursor.execute("INSERT INTO [dbo].[credentials] (usernames, name, normalpass, password, email) VALUES (?, ?, ?, ?, ?)", (usernames, name, normalpass, password, email))
#    conn.commit()

#    # Close the connection
#    conn.close()
#    print("all done")
#    return "User added of success has been added."

# insert_user("khankhan", "khan1", "khan@khan", "pass", "pass")