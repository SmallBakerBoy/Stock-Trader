import mysql.connector as mysql

db = mysql.connect(host="localhost",user="root",passwd="kbf6shVLQten8a",database="Django") 
cursor = db.cursor()

def login():
    pass

def fetch_blacklist(user):
    sql = "SELECT main_blacklist.Ticker FROM auth_user INNER JOIN main_blacklist ON auth_user.ID = main_blacklist.User WHERE auth_user.ID LIKE %s"
    cursor.execute(sql,[user])
    result = cursor.fetchall()
    for i in range(len(result)):
        result[i]=result[i][0]
    return result


