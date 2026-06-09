import pyodbc

def get_connection():
    conn = pyodbc.connect(
        "DRIVER={SQL Server};"
        "SERVER=localhost\\SQLEXPRESS;"
        "DATABASE=HardwareInventory;"
        "Trusted_Connection=yes;"
    )
    return conn