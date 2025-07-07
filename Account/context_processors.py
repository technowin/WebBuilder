from django.conf import settings
from WebBuilder.encryption import *
import Db
from .db_utils import callproc
from django.utils import timezone
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
  
    return {'username':username,'full_name':full_name,'session_timeout_minutes':session_timeout_minutes,'reports':reports, 'menu_items': menu_items}
