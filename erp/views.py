from django.shortcuts import render

# Create your views here.
from django.http import HttpResponse

users = ['gaurav']
passwords = ['gaurav']

def index(request):
    return render(request, 'erp/signin.html')

def dashboard(request):
    user = request.GET['username']
    password = request.GET['password']
    if(user in users and passwords[users.index(user)] == password):
        return render(request,'erp/dashboard.html')
    return render(request, 'erp/register.html')

def register(request):
    return render(request, 'erp/register.html')

def submit(request):
    name = request.GET['fname']
    lname = request.GET['lname']
    mname = request.GET['mname']
    user = request.GET['username']
    password1 = request.GET['password1']
    password2 = request.GET['password2']
    users.append(user)
    passwords.append(password1)
    return render(request, 'erp/signin.html')

