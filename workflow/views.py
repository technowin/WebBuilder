from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
import traceback
import Db 
from workflow.models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone

# Create your views here.

@login_required
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

@login_required        
def GettingStarted(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    try:
        username = request.session.get("username", "")
        
        if request.method == 'GET':
            categories = WebsiteCategory.objects.filter(is_active=1).order_by('id')
            return render(request, 'Workflow/GettingStarted.html', {'categories': categories})
        
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
                        'category_id': category_id,
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
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log",[fun,str(e),request.user.id])  
        print(f"error: {e}")
        messages.error(request, 'Oops...! Something went wrong!')
        response = {'result': 'fail','messages ':'something went wrong !'}  
    
@login_required   
def viewTemplate(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor = m.cursor()

    try:
        username = request.session.get("username", "")
        choice = request.GET.get("choice")
        
        if choice == 'Editing':
            template_id = request.GET.get('template_id')
            category_id = request.GET.get('category_id')

            if not (template_id and category_id):
                messages.error(request, "Missing template or category ID.")
                return redirect('viewTemplate')  # adjust redirect as needed

            # Check if entry already exists
            exists = WebsiteWorkflow.objects.filter(
                template_id=template_id,
                category_id=category_id,
                created_by=username
            ).exists()

            if exists:
                messages.info(request, "This website already exists in your site. Go ahead and edit it!")
                return redirect('mySites')  # or your preferred redirect

            # Create new workflow
            template = WebsiteTemplate.objects.get(id=template_id)
            category = WebsiteCategory.objects.get(id=category_id)

            WebsiteWorkflow.objects.create(
                template=template,
                category=category,
                created_at=timezone.now(),
                created_by=username
            )

            messages.success(request, "Let the magic begin — customize your website your way!")
            return redirect('mySites')

        
    except Exception as e:
        import traceback
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log", [fun, str(e), request.user.id])
        print(f"error: {e}")
        messages.error(request, 'Oops...! Something went wrong!')
   
@login_required   
def mySites(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor = m.cursor()

    try:
        username = request.session.get("username", "")
        workflows = WebsiteWorkflow.objects.select_related('template', 'category').filter(
            created_by=username
        )
        return render(request, 'Workflow/MySites.html', {'workflows': workflows})
    
    except Exception as e:
        import traceback
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        request.user.id and cursor.callproc("stp_error_log", [fun, str(e), request.user.id])
        print(f"Error: {e}")
        messages.error(request, "Oops! Something went wrong.")

   
