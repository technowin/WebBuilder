from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
import traceback
from django.contrib.auth.decorators import login_required
import Db 

# Create your views here.

@login_required
def businessHome(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    try:
        # Your normal logic goes here
        # return render(request, 'Master/Business/BusinessHome.html')
        
        workflow_id = request.GET.get('workflow_id','')
        if workflow_id:
            cursor.callproc("stp_getDataForWebsite", [workflow_id])
            for result in cursor.stored_results():
                workflow_data = list(result.fetchall())
            
            return render(request, 'Master/Business/BusinessHome.html', {"workflow_data": workflow_data})
        else:
            return render(request, 'Master/Business/BusinessHome.html')
    
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log",[fun,str(e),request.user.id])  
        print(f"error: {e}")
        messages.error(request, 'Oops...! Something went wrong!')
        response = {'result': 'fail','messages ':'something went wrong !'}  

@login_required
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

@login_required
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
   
@login_required
def servicepage(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    try:
        # Your normal logic goes here
        return render(request, 'Master/Business/Service.html')
    
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log",[fun,str(e),request.user.id])  
        print(f"error: {e}")
        messages.error(request, 'Oops...! Something went wrong!')
        response = {'result': 'fail','messages ':'something went wrong !'}  
       