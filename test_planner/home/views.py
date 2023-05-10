from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
import mysql.connector
import openpyxl
import pandas
import random

def read_excel(file_path):
    db=mysql.connector.connect(
    host="localhost",
    user="root",
    password="1234",
    database="test_planner"
)
    cursor=db.cursor()
    use_db="use test_planner"
    cursor.execute(use_db)
    cursor.execute("SELECT COUNT(*) FROM QB")
    row = cursor.fetchone()
    total_length = row[0]
    dataf = pandas.read_excel(file_path)
    row=len(dataf)
    column=len(dataf.columns)
    data=dataf.values.tolist()
    for i in range(0,row):
        qno=total_length+1+i
        dept=data[i][1]
        year=data[i][2]
        subject=data[i][3]
        question=data[i][4]
        co=data[i][5]
        cursor.execute(f"INSERT INTO QB VALUES ({qno},\"{dept}\",{year},\"{subject}\",\"{question}\",\"{co}\")")
        optiona=data[i][6]
        optionb=data[i][7]
        optionc=data[i][8]
        optiond=data[i][9]
        cursor.execute(f"INSERT INTO QB_OPTIONS values({qno},'{optiona}','{optionb}','{optionc}','{optiond}')")
        answer=data[i][10]
        cursor.execute(f"INSERT INTO QB_ANS values({qno},'{answer}')")
    db.commit()

def retrieve(dept, year, co, subject):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="test_planner"
    )
    cursor = db.cursor()
    use_db = "use test_planner"
    cursor.execute(use_db)
    cursor.execute(f"SELECT Qid, question from qb where Dept=\"{dept}\" and Year=\"{year}\" and Subject=\"{subject}\"")
    result = cursor.fetchall()
    question_display = random.sample(result, co)
    id = [row[0] for row in question_display]
    question_display = [row[1] for row in question_display]
    optiona = []
    optionb = []
    optionc = []
    optiond = []
    ans = []
    for i in id:
        cursor.execute(f"SELECT optionA from qb_options where Qid={i}")
        result = cursor.fetchall()
        optiona.extend([row[0] for row in result])
    for i in id:
        cursor.execute(f"SELECT optionB from qb_options where Qid={i}")
        result = cursor.fetchall()
        optionb.extend([row[0] for row in result])
    for i in id:
        cursor.execute(f"SELECT optionC from qb_options where Qid={i}")
        result = cursor.fetchall()
        optionc.extend([row[0] for row in result])
    for i in id:
        cursor.execute(f"SELECT optionD from qb_options where Qid={i}")
        result = cursor.fetchall()
        optiond.extend([row[0] for row in result])
    for i in id:
        cursor.execute(f"SELECT answer from qb_ans where Qid={i}")
        result = cursor.fetchall()
        ans.extend([row[0] for row in result])

    questions_data = []
    for i in range(len(question_display)):
        question_data = {
            'Question': question_display[i],
            'OptionA': optiona[i],
            'OptionB': optionb[i],
            'OptionC': optionc[i],
            'OptionD': optiond[i],
            'Answer': ans[i]
        }
        questions_data.append(question_data)

    return questions_data

def add_question(dept, year, subject, question, co, optiona, optionb, optionc, optiond, answer):
    db = mysql.connector.connect(
        host="localhost",
        user="root",
        password="1234",
        database="test_planner"
    )
    cursor = db.cursor()
    use_db = "use test_planner"
    cursor.execute(use_db)
    cursor.execute("SELECT COUNT(*) FROM QB")
    row = cursor.fetchone()
    total_length = row[0]
    qno=total_length+1
    cursor.execute(f"INSERT INTO QB VALUES ({qno},\"{dept}\",{year},\"{subject}\",\"{question}\",\"{co}\")")
    cursor.execute(f"INSERT INTO QB_OPTIONS values({qno},'{optiona}','{optionb}','{optionc}','{optiond}')")
    cursor.execute(f"INSERT INTO QB_ANS values({qno},'{answer}')")
    db.commit()


def home(request):
    if request.method == 'POST':
        dept = request.POST.get('department')
        year = request.POST.get('year')
        q_number = request.POST.get('number')
        subject=request.POST.get('subject')
        file = request.FILES.get('excel')
        file_upload = ""
        deptadd = request.POST.get('departmentadd')
        yearadd = request.POST.get('yearadd')
        subjectadd=request.POST.get('subjectadd')
        question=request.POST.get('question')
        co=request.POST.get('co')
        answer=request.POST.get('answer')
        optiona=request.POST.get('optiona')
        optionb=request.POST.get('optionb')
        optionc=request.POST.get('optionc')
        optiond=request.POST.get('optiond')

        if dept is not None and dept != "" and year is not None and year != "" and q_number is not None and q_number != "" and subject is not None and subject != "":
            q_number = int(q_number)
            result = retrieve(dept, year, q_number, subject)
            context = {
            'dept': dept,
            'year': year,
            'result': result,
            'file_upload': file_upload
        }
        if file:
            read_excel(file)
            file_upload = "Database updated successfully"
            context = {
                'file_upload': file_upload
            }
        if deptadd is not None and deptadd != "" and yearadd is not None and yearadd != "" and subjectadd is not None and subjectadd != "" and question is not None and question != "" and co is not None and co != "" and optiona is not None and optiona != "" and optionb is not None and optionb != "" and optionc is not None and optionc != "" and optiond is not None and optiond != "" and answer is not None and answer != "":
            add_question(deptadd, yearadd, subjectadd, question, co, optiona, optionb, optionc, optiond, answer)
            context = {
                'addquestion': "Added question succesfully"
            }
        template = loader.get_template('index.html')
        return HttpResponse(template.render(context, request))
    else:
        template = loader.get_template('index.html')
        return HttpResponse(template.render({}, request))