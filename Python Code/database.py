import mysql.connector as mysql

db = mysql.connect(host="localhost",user="root",passwd="kbf6shVLQten8a",database="Stock-Trader") 
cursor = db.cursor()

def login():
    pass

def fetch_blacklist(user):
    sql = "SELECT blacklist.Ticker FROM users INNER JOIN blacklist ON users.UserID = blacklist.UserID WHERE users.UserID LIKE %s"
    cursor.execute(sql,[user])
    result = cursor.fetchall()
    return result

print(fetch_blacklist(3))