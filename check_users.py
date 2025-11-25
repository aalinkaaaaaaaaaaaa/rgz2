import sqlite3

def check_users():
    conn = sqlite3.connect('instance/library.db') 
    cursor = conn.cursor()
    
    cursor.execute("SELECT * FROM user")
    users = cursor.fetchall()
    
    print("Список пользователей:")
    for user in users:
        print(user)
    
    conn.close()

if __name__ == "__main__":
    check_users()