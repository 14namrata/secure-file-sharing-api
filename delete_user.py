import sqlite3

email_to_delete = "namratasinghsanjana@gmail.com"

conn = sqlite3.connect("file_sharing.db")
cursor = conn.cursor()

cursor.execute("DELETE FROM users WHERE email = ?", (email_to_delete,))
conn.commit()
conn.close()

print(f"User '{email_to_delete}' deleted.")
