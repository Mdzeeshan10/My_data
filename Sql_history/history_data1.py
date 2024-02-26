import pyodbc
import pandas as pd


class HistSqlDbConnection:
 
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
 
#  def insert_history(self, usernames, name, question, answer ):
   
#    conn = pyodbc.connect(self.conn_str)
#    # Create a cursor from the connection
#    cursor = conn.cursor()
# #    cursor.execute("SET IDENTITY_INSERT [dbo].[history] ON")
#    cursor.execute(f"INSERT INTO [dbo].[history] (usernames, name, question, answer) VALUES ('{usernames}','{name}','{question}','{answer}')")
# #    cursor.execute("SET IDENTITY_INSERT [dbo].[history] OFF")
#    conn.commit()

#    # Close the connection
#    conn.close()
#    return "History of success has been added."
 

 def insert_history(self, usernames, name, question, answer ):
   
   conn = pyodbc.connect(self.conn_str)
   # Create a cursor from the connection
   cursor = conn.cursor()
   # Use ? placeholders for values and provide a tuple of values as the second argument to execute()
   cursor.execute("INSERT INTO [dbo].[history] (usernames, name, question, answer) VALUES (?, ?, ?, ?)", (usernames, name, question, answer))
   conn.commit()

   # Close the connection
   conn.close()
   return "History of success has been added."

 
 def retrieve_history(self, username):
   conn = pyodbc.connect(self.conn_str)

   query = f"select * from dbo.history"
   df = pd.read_sql(query, conn)
   df1 = df.loc[df["usernames"]== username]
   df2 = df1.reset_index(drop=True)
   his_df = df2.sort_values(by='created_at_time',ascending=False)
   main_df = his_df[["name","question", "answer", "created_at_time"]]
   # Close the connection
   conn.close()
   return main_df