import pandas
import numpy
import mysql.connector
import xlrd
import openpyxl
import math
import random


db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="test"
)

cursor=db.cursor()
create_table="CREATE TABLE IF NOT EXISTS question_bank(id int, question varchar(255), co varchar(255), marks int, PRIMARY KEY(id))"
cursor.execute(create_table)
dataf =pandas.read_excel('questions.xlsx')
row=len(dataf)
column=len(dataf.columns)
data=dataf.values.tolist()
for i in range(0,row):
    qno=data[i][0]
    question=data[i][1]
    co=data[i][2]
    marks=data[i][3]
    #print(question)
    cursor.execute(f"INSERT INTO question_bank VALUES ({qno},'{question}',{co},{marks})")
    db.commit()
cursor.execute("ALTER TABLE question_bank ORDER BY co")
co_list=dataf.co.unique()
no_co=len(co_list)
for i in range(0,no_co):
    cursor.execute(f"SELECT question, marks FROM question_bank WHERE co={co_list[i]}")
    result=cursor.fetchall()
    for row in result:
        print(row)
        print("\n")
cursor.execute("DROP TABLE question_bank")



