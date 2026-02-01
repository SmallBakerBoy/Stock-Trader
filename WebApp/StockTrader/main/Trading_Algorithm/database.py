import mysql.connector as mysql
import datetime

db = mysql.connect(host='localhost',user='root',passwd='kbf6shVLQten8a',database='stocktrader') 
cursor = db.cursor()

def fetch_blacklist(user):
    sql = 'SELECT main_blacklist.Ticker FROM auth_user INNER JOIN main_blacklist ON auth_user.ID = main_blacklist.user_id WHERE auth_user.ID LIKE %s'
    cursor.execute(sql,[user])
    result = cursor.fetchall()
    for i in range(len(result)):
        result[i]=result[i][0]
    return result

def get_user_risk(user):
    sql = 'SELECT risk_level FROM auth_user WHERE auth_user.ID LIKE %s'
    cursor.execute(sql,[user])
    result = cursor.fetchall()
    return result

def save_trades(user,trades):
    sql = 'INSERT INTO main_trades (ticker,type,amount,user_id,time) VALUES (%s,%s,%s,%s,%s)'
    for trade in trades:
        cursor.execute(sql,[trade[0],1,trade[1],user,datetime.datetime.now()])
    db.commit()

