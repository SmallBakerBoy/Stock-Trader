import mysql.connector as mysql
import datetime

import json

import yfinance as yf

db = mysql.connect(host='localhost',user='root',passwd='kbf6shVLQten8a',database='stocktrader') 
cursor = db.cursor()

def update_asset(request):
    try:
        decoded = request.decode('utf-8').replace("'",'"')
        body = json.loads(decoded)

        amount = float(body['amount'])
        company = yf.Ticker(body['company'])
        
        if body['type'] == 'sell':
            sql = 'SELECT main_assets.amount FROM main_assets WHERE user_id LIKE %s AND ticker = %s'
            cursor.execute(sql,[body['user'],body['company']])
            result = float(cursor.fetchone()[0])

            if amount > result:
                amount = result

            current_price = company.info.get('currentPrice')
            return sell_asset(body['user'],amount,current_price,body['company'])
        
        elif body['type'] == 'buy':
            sql = 'SELECT main_user.balance FROM main_user WHERE main_user.id LIKE %s'
            cursor.execute(sql,[body['user']])
            balance = float(cursor.fetchone()[0])

            current_price = company.info.get('currentPrice')
            if current_price*amount > balance:
                return 'not enough funds',400
            
            return buy_asset(body['user'],amount,current_price,body['company'])

        else:
            return 'invalid type',400
    except Exception as e:
        return str(e),400

def buy_asset(user,amount,price,ticker):
    cost = amount*price

    try:
        sql = 'SELECT main_assets.amount FROM main_assets WHERE user_id LIKE %s AND ticker = %s'
        cursor.execute(sql,[user,ticker])
        result = cursor.fetchone()
        
        if not result:
            sql = 'INSERT INTO main_assets (ticker,amount,price,user_id) VALUES (%s,%s,%s,%s)'
            cursor.execute(sql,[ticker,amount,price,user])
        else:
            sql = 'UPDATE main_assets SET amount = amount + %s WHERE user_id LIKE %s'
            cursor.execute(sql,[amount,user])

        sql = 'UPDATE main_user SET balance = balance - %s WHERE id LIKE %s'
        cursor.execute(sql,[cost,user])

        db.commit()
        return 'success',200
    except:
        return 'database error',500

def sell_asset(user,amount,price,ticker):
    try:
        sql = 'SELECT main_assets.amount FROM main_assets WHERE user_id LIKE %s AND ticker = %s'
        cursor.execute(sql,[user,ticker])
        result = cursor.fetchone()[0]
        
        if result <= amount:
            sql = 'DELETE FROM main_assets WHERE user_id LIKE %s AND ticker = %s'
            cursor.execute(sql,[user,ticker])
        else:
            sql = 'UPDATE main_assets SET amount = amount - %s WHERE user_id LIKE %s AND ticker = %s'
            cursor.execute(sql,[amount,user,ticker])
        
        value = amount*price
        sql = 'UPDATE main_user SET balance = balance + %s WHERE id LIKE %s'
        cursor.execute(sql,[value,user])
        
        db.commit()
        return 'success',200
    except TypeError:
        return 'asset not owned',400
    except:
        return 'database error',200


def fetch_blacklist(user):
    sql = 'SELECT main_blacklist.Ticker FROM main_user INNER JOIN main_blacklist ON main_user.ID = main_blacklist.user_id WHERE main_user.ID LIKE %s'
    cursor.execute(sql,[user])
    result = cursor.fetchall()
    for i in range(len(result)):
        result[i]=result[i][0]
    return result

def get_user_risk(user):
    sql = 'SELECT risk_level FROM main_user WHERE main_user.ID LIKE %s'
    cursor.execute(sql,[user])
    result = cursor.fetchall()
    return result

def save_trades(user,trades):
    sql = 'INSERT INTO main_trades (ticker,type,amount,user_id,time) VALUES (%s,%s,%s,%s,%s)'
    for trade in trades:
        cursor.execute(sql,[trade[0],1,trade[1],user,datetime.datetime.now()])
    db.commit()

