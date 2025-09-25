import sqlite3

conn = sqlite3.connect("C:/Users/MSI-PC/python/fitness-tracker/todo.db")
cursor = conn.cursor()

cursor.execute("SELECT * FROM users")
users = cursor.fetchall()
print("Users:", users)



conn.close()