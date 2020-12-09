import pymysql
import sys

from database import config
conf = config.config

# PyMySQL Documentation: https://pymysql.readthedocs.io/en/latest/index.html


def connect():
    connection = pymysql.connect(
        user=conf['user'],
        password=conf['password'],
        host=conf['host'],
        port=conf['port'],
        database=conf['database'],
        cursorclass=pymysql.cursors.DictCursor
    )

    return connection


def queryone(sql, fmt=tuple()):
    '''쿼리문을 실행시키고, 찾은 항목 중 첫번째 튜플 반환'''
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(sql, fmt)
        return cur.fetchone()
    except Exception as e:
        print(e)
        raise e
    finally:
        cur.close()
        conn.close()


def queryall(sql, fmt=tuple()):
    '''쿼리문을 실행시키고, 찾은 항목 전체 튜플 리스트 반환'''
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(sql, fmt)
        return cur.fetchall()
    except Exception as e:
        print(e)
        raise e
    finally:
        cur.close()
        conn.close()

def execute(sql, fmt=tuple()):
    '''쿼리문을 실행시키고, 변화를 저장'''
    conn = connect()
    cur = conn.cursor()
    try:
        cur.execute(sql, fmt)
        conn.commit()
    except Exception as e:
        print(e)
        raise e
    finally:
        cur.close()
        conn.close()

def callproc(sql, fmt=tuple()):
    '''프로시져를 실행시키고, 변화를 저장'''
    conn = connect()
    cur = conn.cursor()
    try:
        cur.callproc(sql, fmt)
        message = cur.fetchall()
        conn.commit()
        return message
    except Exception as e:
        print(e)
        raise e
    finally:
        cur.close()
        conn.close()
