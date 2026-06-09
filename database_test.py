# import pyodbc

# try:
#     conn = pyodbc.connect(
#         "DRIVER={SQL Server};"
#         "SERVER=localhost\\SQLEXPRESS;"
#         "DATABASE=HardwareInventory;"
#         "Trusted_Connection=yes;"
#     )

#     print("✅ Connected Successfully!")

#     cursor = conn.cursor()

#     cursor.execute("SELECT * FROM Products")

#     rows = cursor.fetchall()

#     for row in rows:
#         print(row)

#     conn.close()

# except Exception as e:
#     print("❌ Error:", e)