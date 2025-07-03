from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
import traceback
import Db 
from workflow.models import *

# Create your views here.

def workflow_starts(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    try:
        return render(request, 'Workflow/index.html')
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log",[fun,str(e),request.user.id])  
        print(f"error: {e}")
        messages.error(request, 'Oops...! Something went wrong!')
        response = {'result': 'fail','messages ':'something went wrong !'}  
        
def GettingStarted(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    try:
        if request.method == 'GET':
            categories = WebsiteCategory.objects.filter(is_active=1).order_by('id')
            return render(request, 'Workflow/GettingStarted.html', {'categories': categories})
        if request.method == 'POST':
            print("POST request received")
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log",[fun,str(e),request.user.id])  
        print(f"error: {e}")
        messages.error(request, 'Oops...! Something went wrong!')
        response = {'result': 'fail','messages ':'something went wrong !'}  
        
def viewTemplate(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor = m.cursor()

    try:
        if request.method == 'POST':
            category_id = request.POST.get('category_id')

        if category_id:
            try:
                selected_category = WebsiteCategory.objects.get(id=category_id)

                # Check if any templates exist for this category
                templates = WebsiteTemplate.objects.filter(category_id=category_id, is_active=1)

                if templates.exists():
                    return render(request, 'Workflow/viewTemplate.html', {
                        'categoryId': selected_category.id,
                        'categoryName': selected_category.category_name,
                        'templates': templates,
                    })
                else:
                    messages.info(
                        request,
                        "There are currently no templates available under the selected category. Please select a different category. Thank you for your understanding."
                    )
                    return redirect('GettingStarted')

            except WebsiteCategory.DoesNotExist:
                messages.error(request, "Invalid category selected.")
                return redirect('GettingStarted')
        else:
            messages.error(request, "Please select a correct category.")
            return redirect('GettingStarted')
        # if request.method == 'POST':
        #     category_id = request.POST.get('category_id')

        #     if category_id:
        #         try:
        #             selected_category = WebsiteCategory.objects.get(id=category_id)
                    
                    
                    
        #             return render(request, 'Workflow/viewTemplate.html', {
        #                 'categoryId': selected_category.id,
        #                 'categoryName': selected_category.category_name,
        #             })
        #         except WebsiteCategory.DoesNotExist:
        #             messages.error(request, "Invalid category selected.")
        #     else:
        #         messages.error(request, "Please select a correct category.")
        #         return redirect('GettingStarted')

    except Exception as e:
        import traceback
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log", [fun, str(e), request.user.id])
        print(f"error: {e}")
        messages.error(request, 'Oops...! Something went wrong!')
   
