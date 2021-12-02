from django.shortcuts import render, redirect
from django.contrib import messages
import re

# Create your views here.
from django.http import HttpResponse
import mysql.connector
from mysql.connector import errorcode

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'


#mydb = mysql.connector.connect(
 # host="localhost",
 # user="dbms",
#  password="Dbms@1234",
 # database = 'erp'
#)
# mysql -udbms -pdbms -h dbms-mini-project.duckdns.org erp
mydb = mysql.connector.connect(
   host="dbms-mini-project.duckdns.org",
   user="dbms",#root
   password="dbms",#tour
   database = 'erp'
)

loged_in_user_roll = ''
loged_in_user_name = ''
passwords = ['gaurav']

def index(request):
    return render(request, 'erp/index.html')

def login(request):
    #print('here')
    if request.method == 'POST':
        roll_no = request.POST.get('username')
        password = request.POST.get('password')

        mycursor = mydb.cursor()
        sql = "select password,name,is_admitted from students where roll_no = %s"
        mycursor.execute(sql,(roll_no,))

        try:
            user = mycursor.fetchall()[0]
            #print(user)
            mycursor.close() 
            if(password == user[0] and user[2] == 1):
                global loged_in_user_roll,loged_in_user_name
                loged_in_user_roll = roll_no
                loged_in_user_name = user[1]
                #print(user[0], '', password)
                return redirect('/erp/dashboard')
            elif (user[2] == 0):
                return render(request, 'erp/login.html',{'invalid_username' : 'Student not Admitted'})
            return render(request, 'erp/login.html',{'invalid_password' : 'Invalid password'})
        except IndexError:
            return render(request, 'erp/login.html',{'invalid_username' : 'Invalid Username'})

        #print('There')
        #return render(request, 'erp/login.html',{'error' : 'Invalid Credentials'})
    return render(request, 'erp/login.html')


def dashboard(request):
    
    context = {
        'roll' : loged_in_user_roll,
        'name' : loged_in_user_name,
    }
    #print(context)
    return render(request, 'erp/dashboard.html', context)

def register(request):
    print("in register")
    if request.method == 'POST':
        #print("in register POST")
        name = request.POST.get('name')
        roll_no = request.POST.get('roll')
        year = request.POST.get('year')
        mail = request.POST.get('mail')
        contact = request.POST.get('contact')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        #print(name ,'', roll_no ,'', year,'',mail,'',contact,'',password1, '',password2 )

        error = 0
        context = {
            'error1' : '',
            'error2' : '',
            'error3' : '',
            'error4' : '',
            'error5' : '',
        }

        try : 
            mycursor = mydb.cursor()
            sql = "select roll_no from students"
            mycursor.execute(sql)
            roll = mycursor.fetchall()[0]
            #print(roll)
            mycursor.close() 
        
            if(roll_no in roll):
                #print(roll[0], '', roll_no)
                context['error1'] = 'user allready Registerd' 
                error = 1
                #return render(request, 'erp/register.html',{'error1' : 'user allready Registerd'})
        except IndexError :
            pass
        if((roll_no[ : 1].isdigit() == False) or (roll_no[2 : 3].isalpha() == False) or (roll_no[4 : ].isdigit() == False)):
            print(roll_no)
            error = 1
            context['error1'] = 'Invalid Username'

        if ((contact.isdigit()==False) or (len(str(contact))!=10)):
            context['error2'] = 'Enter Valid phone number'
            error = 1
            #return render(request, 'erp/register.html', {'error2' : 'Enter Valid phone number'})
        
        if (password1 != password2):
            context['error3'] = 'passwords do not matched'
            error = 1
            #return render(request, 'erp/register.html', {'error3' : 'passwords do not matched'})

        if(re.fullmatch(regex, mail) == False):
            context['error4'] = 'Invalid Mail'
            error = 1
            #return render(request, 'erp/register.html', {'error4' : 'Invalid Mail'})

        if(error == 1):
            return render(request, 'erp/register.html', context)

        mycursor = mydb.cursor() 
        sql = 'insert into students(Roll_no,name,contact_no,mail_id,year,password,is_admitted) values(%s,%s,%s,%s,%s,%s,%s)'   
        val = (roll_no,name,contact,mail,year,password1,0)

        mycursor.execute(sql, val)
        mydb.commit()

        return redirect('/erp/login')
    return render(request, 'erp/register.html')

def teacher(request):
    print('here')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        mycursor = mydb.cursor()
        sql = "select name,password from teacher where name = %s"
        mycursor.execute(sql,(username,))

        try:
            user = mycursor.fetchall()[0]
            #print(user)
            mycursor.close() 
            if(password == user[1]):
                global loged_in_user_roll,loged_in_user_name
                loged_in_user_roll = id
                loged_in_user_name = user[0]
                #print(user[1], '', password)
                return redirect('/erp/teacher-dashboard')
            return render(request, 'erp/teacher.html',{'invalid_password' : 'Invalid password'})
        except IndexError:
            return render(request, 'erp/teacher.html',{'invalid_username' : 'Invalid Username'})
        #print('There')
        #return render(request, 'erp/login.html',{'error' : 'Invalid Credentials'})
    return render(request, 'erp/teacher.html')

def teacher_dashboard(request):
    return render(request, 'erp/teacher_dashboard.html')

def admin(request):
    #print('here')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        mycursor = mydb.cursor()
        sql = "select username,password from admin where username = %s"
        mycursor.execute(sql,(username,))

        try:
            user = mycursor.fetchall()[0]
            #print(user)
            mycursor.close() 
            if(password == user[1]):
                global loged_in_user_roll,loged_in_user_name
                loged_in_user_roll = id
                loged_in_user_name = user[0]
                #print(user[1], '', password)
                return redirect('/erp/admin-dashboard')
            return render(request, 'erp/admin.html',{'invalid_password' : 'Invalid password'})
        except IndexError:
            return render(request, 'erp/admin.html',{'invalid_username' : 'Invalid Username'})

    return render(request, 'erp/admin.html')

def admin_dashboard(request):
    mycursor = mydb.cursor()
    sql = "select * from students where is_admitted = %s"
    status = 0
    mycursor.execute(sql,(status,))
    #print(mycursor)
    students = [{'roll':x[0], 'name':x[1], 'contact' : x[2], 'mail' : x[3], 'dept' : x[4], 'year' : x[5]} for x in mycursor.fetchall()]
    #print(students)
    mycursor.close()

    mycursor = mydb.cursor()
    sql = "select * from students where is_admitted = %s"
    status = 1
    mycursor.execute(sql,(status,))
    #print(mycursor)
    admitted_students = [{'roll':x[0], 'name':x[1], 'contact' : x[2], 'mail' : x[3], 'dept' : x[4], 'year' : x[5]} for x in mycursor.fetchall()]
    #print(admitted_students)
    mycursor.close()

    mycursor = mydb.cursor()
    mycursor.execute('select name from teacher')
    teachers =[{'name' : x[0]} for x in mycursor.fetchall()]
    #print(teachers)
    mycursor.close()

    mycursor = mydb.cursor()
    mycursor.execute('select username from admin')
    admins =[{'name' : x[0]} for x in mycursor.fetchall()]
    #print(teachers)
    mycursor.close()
    return render(request, 'erp/admin_dashboard.html',{'students' : students, 'admitted_students' : admitted_students, 'teachers' : teachers, 'admins' : admins})

def acceptUser(request):
    if request.method == 'POST':
        roll_no = request.POST.get('roll')
        method = request.POST.get('action') 
        mycursor = mydb.cursor()
        query = "update students set is_admitted = 1 where roll_no = %s"
        mycursor.execute(query,(roll_no,))
        mydb.commit()
        return redirect('/erp/admin-dashboard')
    return HttpResponse("User Updation Failed")

def rejectUser(request):
    if request.method == 'POST':
        roll_no = request.POST.get('roll')
        #method = request.POST.get('action') 
        mycursor = mydb.cursor()
        query = "delete from students where roll_no = %s"
        mycursor.execute(query,(roll_no,))
        mydb.commit()
        return redirect('/erp/admin-dashboard')
    return HttpResponse("User Rejection Failed")

def add_teacher(request):
    #print("In Add teacher")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        mycursor = mydb.cursor()
        sql = 'select name from teacher where name = %s'
        mycursor.execute(sql,(username,))
        try :
            user = mycursor.fetchall()[0]
            #print(user)
            mycursor.close()
            if(username in user):
                return render(request,'erp/add_teacher.html',{'invalid_username' : 'teacher all ready exist'})
        except IndexError:
            sql = 'insert into teacher(name,password) values(%s,%s)'   
            val = (username,password)
            mycursor.execute(sql, val)
            mydb.commit()
            #print("teacher added")
            return redirect("/erp/admin-dashboard")
    return render(request, 'erp/add_teacher.html')

def add_admin(request):
    print("In Add admin")
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        mycursor = mydb.cursor()
        sql = 'select username from admin where username = %s'
        mycursor.execute(sql,(username,))
        try :
            user = mycursor.fetchall()[0]
            print(user)
            mycursor.close()
            if(username in user):
                return render(request,'erp/add_teacher.html',{'invalid_username' : 'teacher all ready exist'})
        except IndexError:
            sql = 'insert into admin(username,password) values(%s,%s)'   
            val = (username,password)
            mycursor.execute(sql, val)
            mydb.commit()
            print("admin added")
            return redirect("/erp/admin-dashboard")
    return render(request, 'erp/add_admin.html')

def remove_teacher(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        #method = request.POST.get('action') 
        mycursor = mydb.cursor()
        query = "delete from teacher where name = %s"
        mycursor.execute(query,(name,))
        mydb.commit()
        return redirect('/erp/admin-dashboard')
    return HttpResponse("Teacher Deletion Failed Failed")    

def delete_admin(request):
    if request.method == 'POST':
        name = request.POST.get('username')
        #method = request.POST.get('action') 
        mycursor = mydb.cursor()
        mycursor.execute('select username from admin')
        admin = mycursor.fetchall()
        #print(admin)
        if (len(admin) == 1):
            return redirect('/erp/admin-dashboard')
        query = "delete from admin where username = %s"
        mycursor.execute(query,(name,))
        mydb.commit()
        return redirect('/erp/admin-dashboard')
    return HttpResponse("Teacher Deletion Failed Failed")    


