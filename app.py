from typing import Text
from flask import Flask,render_template,request
#library to connect to database
import pymysql


app = Flask(__name__)
connection = ""
cur = ""
#Function to connect to the database 
#cmd-  mysql-h localhost -u root
#use pythonmysql


def connectToDB():
    global connection,cur
    connection = pymysql.connect(host="localhost",user="root",password="", database="lib_management")
    cur=connection.cursor()
    print("Database Connected")

def disconnectDB():
    cur.close()
    connection.close()
    print("Database Disconnected")

def getAllstudents():
    select_query = "SELECT * FROM student_info;"
    cur.execute(select_query)
    #all records --> cur.fetchall
    #few records-->cur.fetchmany(number)
    #only one record-->cur.fetchone()
    data = cur.fetchall()
    #print(data)
    return data

def getonestudent(Sr_no):
    select_query = "SELECT * FROM student_info WHERE Sr_no= %s;"
    cur.execute(select_query, (Sr_no, ))
    data = cur.fetchone()
    #print(data)
    return data

def view():
    view_query="SELECT * FROM student_info;"
    cur.execute(view_query)
    data = cur.fetchall()
    return data

def attend(sSr_no):
    attend_query="SELECT * FROM student_info;"
    cur.execute(attend_query)
    data = cur.fetchall()
    return data

def Present_Student(sSr_no):
    try:
        present_query="UPDATE student_info SET Attendance = 'Present' WHERE Sr_no =%s;"
        print(present_query)
        print(sSr_no)
        cur.execute(present_query,(sSr_no ))
        connection.commit()
        return True
    except:
        return False
    
def Absent_Student(sSr_no):
    try:
        absent_query="UPDATE student_info SET Attendance = 'Absent' WHERE  Sr_no =%s;"
        cur.execute(absent_query,(sSr_no ))
        connection.commit()
        return True
    except:
        return False


def insertStudent(sname,semail,smobile,sbook_name,sbook_author,sdateofissue,status):
    try:
        insert_query="INSERT INTO student_info(name, email, mobile, book_name, book_author, dateofissue,status) VALUES(%s, %s, %s, %s, %s, %s, %s);"
        print(sdateofissue)
        cur.execute(insert_query,(sname,semail,smobile,sbook_name,sbook_author,sdateofissue,status))
        #print(sname,semail,smobile,sbook_name,sbook_author,sdateofissue)
        connection.commit()
        return True
    except:
        return False

def Update(sname,semail,smobile,sbook_name,sbook_author,sdateofissue,status,sSr_no):
    try:
        update_query= "UPDATE student_info SET name=%s, email=%s, mobile=%s, book_name=%s, book_author=%s,dateofissue=%s, status= %s WHERE Sr_no=%s;"
        cur.execute(update_query,(sname,semail,smobile,sbook_name,sbook_author,sdateofissue,status,sSr_no))
        connection.commit()
        return True
    except:
        return False


def deleteStudent(sSr_no):
    try:
        delete_query="DELETE from student_info where Sr_no =%s;"
        cur.execute(delete_query,(sSr_no, ))
        connection.commit()
        return True
    except:
        return False
#Write function for URL call
#URL calls in web are called routes
#Http methoda inorder to call the url are Get and post

#index route:
@app.route("/",methods=['Get','POST'])

def index():
    html_data = {}
    connectToDB()   
    students= getAllstudents()
    html_data['stud_list'] = students
    disconnectDB() 
    #return "<h1>Hello Flask Programming</h1>"
    return render_template("index.html",data = html_data)

@app.route("/view/",methods=['Get','POST'])

def view():
    html_data = {}
    connectToDB()   
    students= getAllstudents()
    html_data['stud_list'] = students
    disconnectDB() 
    #return "<h1>Hello Flask Programming</h1>"
    return render_template("view.html",data = html_data)

@app.route("/attend/",methods=['Get'])
def attend_student():
    connectToDB()
    html_data = {}
    Sr_no=request.args.get('rn', type=int, default=1)
    if attend(Sr_no):
        html_data['success'] = 'Attendance marked successfully'
    else:
        html_data['error'] = 'Unable to mark attendance'
    html_data['stud_list'] = getAllstudents()
    disconnectDB()
    return render_template("attend.html", data = html_data)

@app.route("/edit/",methods=['GET','POST'])
def update_student_details():
    connectToDB()
    if request.method =='GET':
        #print(request.args.get('rn', type=int, default=1))
        Sr_no = request.args.get('rn', type=int, default=1)
        data= getonestudent(Sr_no) 
        disconnectDB()  
        return render_template("update.html",student_info = data)
    if request.method == "POST":
        form_data = request.form
        name = form_data.get("txtName")
        email = form_data.get("txtEmail")
        mobile = form_data.get("txtMobile")
        book_name = form_data.get("txtBookName")
        book_author = form_data.get("txtBookAuth")
        dateofissue = form_data.get("txtdateofissue")
        status = form_data.get("txtStatus")
        Sr_no = form_data.get("txtSr_no")

        html_data = {}
        if Update(name, email, mobile, book_name, book_author, dateofissue,status, Sr_no):    
            html_data['success']='Record updated successfully.'
        else:
            html_data['error'] = 'Unable to update the record'
        html_data['stud_list'] = getAllstudents()
        disconnectDB()
        return render_template("index.html",data = html_data)
    return "Update form"



@app.route("/delete/",methods=['GET'])

def delete_student_record():
    connectToDB()
    html_data = {}
    Sr_no=request.args.get('rn', type=int, default=1)
    
    if deleteStudent(Sr_no):
        html_data['success'] = 'Record deleted successfully'
    else:
        html_data['error'] = 'Unable to delete record'
    html_data['stud_list'] = getAllstudents()
    disconnectDB()
    return render_template("index.html", data = html_data)

@app.route("/present/",methods=['GET'])

def present():
    connectToDB()
    html_data = {}
    sSr_no=request.args.get('sn', type= int )
    
    if Present_Student(sSr_no):
        html_data['success'] = 'Attendence Marked successfully'
    else:
        html_data['error'] = 'Unable to mark attendance'
    html_data['stud_list'] = getAllstudents()
    disconnectDB()
    return render_template("attend.html", data = html_data)  
     
@app.route("/absent/",methods=['GET'])
def absent():
    connectToDB()
    html_data = {}
    Sr_no=request.args.get('sn', type=int)
    
    if Absent_Student(Sr_no):
        html_data['success'] = 'Attendence Marked successfully'
    else:
        html_data['error'] = 'Unable to mark attendance'
    html_data['stud_list'] = getAllstudents()
    disconnectDB()
    return render_template("attend.html", data = html_data)   



@app.route("/insert/",methods=['GET','POST'])    
def insert_student_record():
    if request.method == 'GET':
        return render_template("insert.html")
    if request.method == "POST":
        connectToDB()
        html_data={}
        form_data = request.form
        print(form_data)
        name = form_data.get("txtName")
        email = form_data.get("txtEmail")
        mobile = form_data.get("txtMobile")
        book_name = form_data.get("txtBookName")
        book_author = form_data.get("txtBookAuth")
        dateofissue = form_data.get("txtdateofissue")
        status = form_data.get("txtStatus")
        #call function to insert data
        if insertStudent(name,email,mobile,book_name,book_author,dateofissue,status):
            html_data['success'] = "{} Student's record stored successfully.".format(name)
        else:
            html_data['error'] = "Couldn't save the data, please try again!"
        html_data['stud_list']= getAllstudents()
        disconnectDB()
        return render_template("index.html",data = html_data)
if __name__ == "__main__":
    app.run()