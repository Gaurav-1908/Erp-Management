from django.shortcuts import render, redirect
from django.contrib import messages
import re

# Create your views here.
from django.http import HttpResponse
import mysql.connector
from mysql.connector import errorcode

regex = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'



mydb = mysql.connector.connect(
  host="localhost",
  user="dbms",
  password="Dbms@1234",
  database = 'erp'
)

loged_in_user_roll = ''
loged_in_user_name = ''
passwords = ['gaurav']

def index(request):
    return render(request, 'erp/index.html')

def login(request):
    print('here')
    if request.method == 'POST':
        roll_no = request.POST.get('username')
        password = request.POST.get('password')

        mycursor = mydb.cursor()
        sql = "select password,name from students where roll_no = %s"
        mycursor.execute(sql,(roll_no,))

        try:
            user = mycursor.fetchall()[0]
            print(user)
            mycursor.close() 
            if(password == user[0]):
                global loged_in_user_roll,loged_in_user_name
                loged_in_user_roll = roll_no
                loged_in_user_name = user[1]
                print(user[0], '', password)
                return redirect('/erp/dashboard')
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
    print(context)
    return render(request, 'erp/dashboard.html', context)

def register(request):
    print("in register")
    if request.method == 'POST':
        print("in register POST")
        name = request.POST.get('name')
        roll_no = request.POST.get('roll')
        year = request.POST.get('year')
        mail = request.POST.get('mail')
        contact = request.POST.get('contact')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        print(name ,'', roll_no ,'', year,'',mail,'',contact,'',password1, '',password2 )

        mycursor = mydb.cursor()
        sql = "select roll_no from students"
        mycursor.execute(sql)
        roll = mycursor.fetchall()[0]
        print(roll)
        mycursor.close() 
        error = 0
        context = {
            'error1' : '',
            'error2' : '',
            'error3' : '',
            'error4' : '',
            'error5' : '',
        }
        if(roll_no in roll):
            print(roll[0], '', roll_no)
            context['error1'] = 'user allready Registerd' 
            error = 1
            #return render(request, 'erp/register.html',{'error1' : 'user allready Registerd'})
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
        sql = 'insert into students(Roll_no,name,contact_no,mail_id,year,password) values(%s,%s,%s,%s,%s,%s)'   
        val = (roll_no,name,contact,mail,year,password1)

        mycursor.execute(sql, val)
        mydb.commit()

        return redirect('/erp/login')
    return render(request, 'erp/register.html')

def teacher(request):
    print('here')
    if request.method == 'POST':
        id = request.POST.get('username')
        password = request.POST.get('password')

        mycursor = mydb.cursor()
        sql = "select name,password from teacher where id = %s"
        mycursor.execute(sql,(id,))

        try:
            user = mycursor.fetchall()[0]
            print(user)
            mycursor.close() 
            if(password == user[1]):
                global loged_in_user_roll,loged_in_user_name
                loged_in_user_roll = id
                loged_in_user_name = user[0]
                print(user[1], '', password)
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
    print('here')
    if request.method == 'POST':
        id = request.POST.get('username')
        password = request.POST.get('password')

        mycursor = mydb.cursor()
        sql = "select id,password from admin where id = %s"
        mycursor.execute(sql,(id,))

        try:
            user = mycursor.fetchall()[0]
            print(user)
            mycursor.close() 
            if(password == user[1]):
                global loged_in_user_roll,loged_in_user_name
                loged_in_user_roll = id
                loged_in_user_name = user[0]
                print(user[1], '', password)
                return redirect('/erp/teacher-dashboard')
            return render(request, 'erp/teacher.html',{'invalid_password' : 'Invalid password'})
        except IndexError:
            return render(request, 'erp/teacher.html',{'invalid_username' : 'Invalid Username'})

    return render(request, 'erp/admin.html')

def admin_dashboard(request):
    return render(request, 'erp/admin_dashboard.html')

