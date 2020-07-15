import os
from datetime import datetime
import sqlite3
from sqlite3 import Error
print("Current Time: " +  str(datetime.now()))

database = 'database.db'
def create_connection(db_file):
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        print(sqlite3.version)
    except Error as e:
        print(e)

    return conn
def create_table(conn, create_table_sql):
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)
def create_user(conn, user):
    sql = ''' INSERT INTO users(user_username, user_password, created_date)
              VALUES(?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, user)
    conn.commit()
    return cur.lastrowid
def create_message(conn, message):
    sql = ''' INSERt INTO messages(content,sender, sent_date)
              VALUES(?, ?, ?) '''
    cur = conn.cursor()
    cur.execute(sql, message)
    conn.commit
    return cur.lastrowid
def create_user_panel(conn):
    conn = create_connection(database)
    print("")
    print("User Creation Panel:")
    username = input("Username: ")
    password = input("Password: ")
    cur = conn.cursor()
    cur.execute("SELECT user_password FROM users WHERE user_username=?", (username,))
    search_user = cur.fetchall()

    if search_user:
        print("Username already Exists \n")
        login(conn)
    else:
        with conn:
            user_query = (username, password, str(datetime.now()))
            create_user(conn, user_query)
            login(conn)
def login(conn):
    print("User Login Panel")
    print("To Create a user, insert into username: 'user.create'")
    print("")
    login_user = input("Username: ")

    if login_user == "user.create":
        create_user_panel(conn)
    login_pass = input("Password: ")
    cur = conn.cursor()
    password_list = cur.execute("SELECT user_password FROM users WHERE user_username=?", (login_user,)).fetchone()
    print(password_list[0])

    if password_list[0] != login_pass:

        print("\n Incorrect Password!")
        current_user = "Guest"

    else:
        current_user = login_user
    main(current_user)
def send_message(conn, current_user):
    with conn:
        message = input("$ ")
        message_query = (message, current_user, str(datetime.now()))
        create_message(conn, message_query)
    main(conn)
def get_messages(conn):
    cur = conn.cursor()
    messages = cur.execute("SELECT content, sender, sent_date FROM messages").fetchall()

    for message in messages:
        print(message)

def main(current_user):
    conn = create_connection(database)
    sql_create_users_table = """ CREATE TABLE IF NOT EXISTS users (
                                        id integer PRIMARY KEY,
                                        user_username text NOT NULL,
                                        user_password text NOT NULL,
                                        created_date datetime NOT NULL
                                    ); """
    sql_create_messages_table = """CREATE TABLE IF NOT EXISTS messages (
                                    id integer PRIMARY KEY,
                                    content text NOT NULL,
                                    sender text NOT NULL,
                                    sent_date datetime NOT NULL
                                );"""
    
    if conn is not None:
        create_table(conn, sql_create_users_table)
        create_table(conn, sql_create_messages_table)


    if current_user is "Guest":
        login(conn)
    else:
        os.system('clear')

    get_messages(conn)
    send_message(conn, current_user)


if __name__ == '__main__':
    current_user = "Guest"
    main(current_user)
