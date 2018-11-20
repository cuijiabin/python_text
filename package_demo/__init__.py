# coding=utf-8
import pymysql


def hi():
    print("hi")


def get_mia_cursor(db_name="mia_mirror"):
    conn = pymysql.connect(host="10.1.3.33",
                           port=3306,
                           user="pop_cuijiabin",
                           passwd="8dtx5EOUZASc#",
                           db=db_name,
                           charset="utf8")
    return conn.cursor()
