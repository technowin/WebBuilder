from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
import traceback
import Db 

# Create your views here.

def businessHome(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    try:
        # Your normal logic goes here
        return render(request, 'Master/Business/BusinessHome.html')
    
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log",[fun,str(e),request.user.id])  
        print(f"error: {e}")
        messages.error(request, 'Oops...! Something went wrong!')
        response = {'result': 'fail','messages ':'something went wrong !'}  
       
def BusinessContactUs(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    try:
        # Your normal logic goes here
        return render(request, 'Master/Business/BusinessContactUs.html')
    
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log",[fun,str(e),request.user.id])  
        print(f"error: {e}")
        messages.error(request, 'Oops...! Something went wrong!')
        response = {'result': 'fail','messages ':'something went wrong !'}  
        
def aboutUs(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    try:
        # Your normal logic goes here
        return render(request, 'Master/Business/AboutUs.html')
    
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log",[fun,str(e),request.user.id])  
        print(f"error: {e}")
        messages.error(request, 'Oops...! Something went wrong!')
        response = {'result': 'fail','messages ':'something went wrong !'}  
       