from django.conf import settings
from WebBuilder.encryption import *
import Db
from .db_utils import callproc
from django.utils import timezone
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
import traceback
from django.contrib.auth.decorators import login_required
import Db 

def logged_in_user(request):
    user =''
    session_cookie_age_seconds = settings.AUTO_LOGOUT['IDLE_TIME']
    session_timeout_minutes = session_cookie_age_seconds 
    username = request.session.get('username', '')
    full_name = request.session.get('full_name', '')
    user_id = request.session.get('user_id', '')
    role_id = request.session.get('role_id', '')
    if request.user.is_authenticated ==True:
        user = str(request.user.id or '')
    reports = ''    
    menu_items = []
    
    workflow_data = []
    workflow_id = request.GET.get('workflow_id', '')
    
    if workflow_id:
        try:
            m = Db.get_connection()
            if not m.is_connected():
                m.reconnect()
            cursor = m.cursor()
            cursor.callproc("stp_getDataForWebsite", [workflow_id])
            for result in cursor.stored_results():
                workflow_data = result.fetchall()
            
        except Exception as e:
            print("DB error:", e)
        finally:
            if cursor: cursor.close()
            if m and m.is_connected(): m.close()
    return {'username':username,'full_name':full_name,'session_timeout_minutes':session_timeout_minutes,'reports':reports, 'menu_items': menu_items, 'workflow_data': workflow_data}
