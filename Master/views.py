from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
import traceback
from django.contrib.auth.decorators import login_required
import Db 
from collections import defaultdict
from workflow.models import *
from django.core.mail import send_mail
from django.conf import settings
from django.http import JsonResponse
import os
from collections import defaultdict
from django.core.paginator import Paginator
from django.shortcuts import render, get_object_or_404

# Create your views here.

# @login_required
# def businessHome(request):
#     Db.closeConnection()
#     m = Db.get_connection()
#     cursor=m.cursor()
#     try:
#         # Your normal logic goes here
#         # return render(request, 'Master/Business/BusinessHome.html')
        
#         workflow_id = request.GET.get('workflow_id', '')

#         if workflow_id:
#             cursor.callproc("stp_getDataForWebsite", [workflow_id])
#             for result in cursor.stored_results():
#                 workflow_data = list(result.fetchall())
                
#             cursor.callproc("stp_geSectionWiseDataForWebsite", [workflow_id])

#             for result in cursor.stored_results():
#                 raw_data = list(result.fetchall())
#                 columns = [col[0] for col in result.description]

#             # Convert each row to a dict
#             data_list = [dict(zip(columns, row)) for row in raw_data]

#             # Group by 'section_title'
#             section_data = defaultdict(list)
#             for item in data_list:
#                 section_title = item.get('section_title')
#                 if not section_title or not section_title.strip():
#                     section_title = 'Others'
#                 section_data[section_title].append(item)

                
#             formatted_data = {}
#             for key, val in section_data.items():
#                 formatted_key = key.replace(" ", "_")  # "Main Slider" -> "Main_Slider"
#                 formatted_data[formatted_key] = val
            
#             return render(request, 'Master/Business/BusinessHome.html',
#                           {"workflow_data": workflow_data,
#                             "section_data": formatted_data,
#                             "workflow_id": workflow_id})
#         else:
#             return render(request, 'Master/Business/BusinessHome.html')
    
#     except Exception as e:
#         tb = traceback.extract_tb(e.__traceback__)
#         fun = tb[0].name
#         cursor.callproc("stp_error_log",[fun,str(e),request.user.id])  
#         print(f"error: {e}")
#         messages.error(request, 'Oops...! Something went wrong!')
#         response = {'result': 'fail','messages ':'something went wrong !'}  

@login_required
def BusinessContactUs(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    try:
        workflow_id = request.GET.get('workflow_id', '')
        if workflow_id:
            
            cursor.callproc("stp_getDataForWebsite", [workflow_id])
            for result in cursor.stored_results():
                workflow_data = list(result.fetchall())
            return render(request, 'Master/Business/BusinessContactUs.html',
                {
                    "workflow_data": workflow_data,
                    "workflow_id":workflow_id
                })
        else:
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
        
        workflow_id = request.GET.get('workflow_id', '')
        if workflow_id:
            
            cursor.callproc("stp_getDataForWebsite", [workflow_id])
            for result in cursor.stored_results():
                workflow_data = list(result.fetchall())
                
            cursor.callproc("stp_geSectionWiseDataForWebsite", [workflow_id])

            for result in cursor.stored_results():
                raw_data = list(result.fetchall())
                columns = [col[0] for col in result.description]

            # Convert each row to a dict
            data_list = [dict(zip(columns, row)) for row in raw_data]

            # Group by 'section_title'
            section_data = defaultdict(list)
            for item in data_list:
                section_title = item.get('section_title')
                if not section_title or not section_title.strip():
                    section_title = 'Others'
                section_data[section_title].append(item)
                
            formatted_data = {}
            for key, val in section_data.items():
                formatted_key = key.replace(" ", "_")  # "Main Slider" -> "Main_Slider"
                formatted_data[formatted_key] = val
                
            return render(request, 'Master/Business/AboutUs.html',
                          {"workflow_data": workflow_data,
                           "section_data": formatted_data,
                            "workflow_id": workflow_id
                          })
        else:
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
        workflow_id = request.GET.get('workflow_id', '')
        if workflow_id:
            
            cursor.callproc("stp_getDataForWebsite", [workflow_id])
            for result in cursor.stored_results():
                workflow_data = list(result.fetchall())
                
            cursor.callproc("stp_geSectionWiseDataForWebsite", [workflow_id])

            for result in cursor.stored_results():
                raw_data = list(result.fetchall())
                columns = [col[0] for col in result.description]

            # Convert each row to a dict
            data_list = [dict(zip(columns, row)) for row in raw_data]

            # Group by 'section_title'
            section_data = defaultdict(list)
            for item in data_list:
                section_title = item.get('section_title')
                if not section_title or not section_title.strip():
                    section_title = 'Others'
                section_data[section_title].append(item)
                
            formatted_data = {}
            for key, val in section_data.items():
                formatted_key = key.replace(" ", "_")  # "Main Slider" -> "Main_Slider"
                formatted_data[formatted_key] = val
                
            return render(request, 'Master/Business/Service.html',
                          {"workflow_data": workflow_data,
                           "section_data": formatted_data,
                            "workflow_id": workflow_id
                          })
            
        else:
            return render(request, 'Master/Business/Service.html')
    
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log",[fun,str(e),request.user.id])  
        print(f"error: {e}")
        messages.error(request, 'Oops...! Something went wrong!')
        response = {'result': 'fail','messages ':'something went wrong !'}  

@login_required
def ourProduct(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    try:
        workflow_id = request.GET.get('workflow_id', '')
        page_number = request.GET.get('page', 1)
        
        if workflow_id:
            cursor.callproc("stp_getDataForWebsite", [workflow_id])
            for result in cursor.stored_results():
                workflow_data = list(result.fetchall())

            cursor.callproc("stp_geSectionWiseDataForWebsite", [workflow_id])
            for result in cursor.stored_results():
                raw_data = list(result.fetchall())
                columns = [col[0] for col in result.description]

            # Convert to dict
            data_list = [dict(zip(columns, row)) for row in raw_data]

            # Group by section
            section_data = defaultdict(list)
            for item in data_list:
                section = item.get('section_title', 'Others').strip() or 'Others'
                section_data[section].append(item)

            formatted_data = {}
            for key, val in section_data.items():
                formatted_key = key.replace(" ", "_")
                formatted_data[formatted_key] = val

            # Handle pagination only for Our_Product
            our_products = formatted_data.get('Our_Product', [])
            paginator = Paginator(our_products, 4)  # 4 items per page
            page_obj = paginator.get_page(page_number)

            formatted_data['Our_Product_Paginated'] = page_obj

            return render(request, 'Master/Business/ourProduct.html', {
                "workflow_data": workflow_data,
                "section_data": formatted_data,
                "workflow_id": workflow_id,
                "page_obj": page_obj,
            })
            
        else:
            return render(request, 'Master/Business/ourProduct.html')
    
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log",[fun,str(e),request.user.id])  
        print(f"error: {e}")
        messages.error(request, 'Oops...! Something went wrong!')
        response = {'result': 'fail','messages ':'something went wrong !'}  
   
@login_required
def send_contact_email(request):
    try:
        if request.method == 'POST':
            username = request.session.get("username", "")
            name = request.POST.get('name')
            email = request.POST.get('email')
            subject = request.POST.get('subject')
            message = request.POST.get('message')
            workflow_id = request.POST.get('workflow_id')

            # Validate fields
            if not all([name, email, subject, message]):
                messages.error(request, "All fields are required.")
                return redirect(f"/BusinessContactUs?workflow_id={workflow_id}")  # Replace with your actual contact page URL name

            # Save contact message using Django ORM
            contact_message = ContactMessage.objects.create(
                name=name,
                email=email,
                subject=subject,
                message=message,
                created_by=username
            )

            # Send email
            send_mail(
                subject=f"Contact Form Submission: {subject}",
                message=f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}",
                from_email=settings.DEFAULT_FROM_EMAIL,
                recipient_list=[settings.CONTACT_EMAIL],
                fail_silently=False,
            )

            messages.success(request, 'Your message has been sent successfully.')
            return redirect(f"/BusinessContactUs?workflow_id={workflow_id}")

        else:
            messages.error(request, "Invalid request method.")
            return redirect(f"/BusinessContactUs?workflow_id={workflow_id}")

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name

        try:
            from . import Db  # assuming your Db helper is in the same app
            Db.closeConnection()
            m = Db.get_connection()
            cursor = m.cursor()
            if request.user.id:
                cursor.callproc("stp_error_log", [fun, str(e), request.user.id])
            cursor.close()
            m.commit()
        except Exception as db_log_err:
            print("Error while logging error:", db_log_err)

        print(f"Error: {e}")
  
@login_required
def view_document_master(request):
        
    workflow_id = request.GET.get("workflow_id") 
    doc_type = request.GET.get("doc_type")
    doc_path = request.GET.get("doc_path")
    try:
        if doc_type == 'pdf':
            file_field = doc_path
        else:
            return JsonResponse({'error': 'Invalid document type.'}, status=400)
        if file_field:
            return JsonResponse({
                'file_url': os.path.join(settings.MEDIA_URL, file_field)
            }, status=200)
        else:
            return JsonResponse({'error': 'File not uploaded.'}, status=404)
    except WebsiteWorkflow.DoesNotExist:
        return JsonResponse({'error': 'Workflow not found.'}, status=404)

# @login_required
def businessHome(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor=m.cursor()
    try:
        workflow_id = getattr(getattr(request, "workflow", None), "id", None)
        # fallback to GET param (optional, for testing/debug)
        if not workflow_id:
            workflow_id = request.GET.get('workflow_id', '')
        
        # workflow_id = request.GET.get('workflow_id', '')
        page_number = request.GET.get('page', 1)
        slug = request.GET.get('slug', '')

        if workflow_id:
            
            # page = Page.objects.filter(is_active=1, website_id=workflow_id).first()
            if slug:
                page = Page.objects.filter(is_active=1, website_id=workflow_id, slug__iexact=slug).first()
            else:
                page = Page.objects.filter(is_active=1, website_id=workflow_id).first()

            print(f"Page: {page}")
            
            cursor.callproc("stp_getDataForWebsite", [workflow_id])
            for result in cursor.stored_results():
                workflow_data = list(result.fetchall())
                
            page_data = [] 
            
            if workflow_id:
                cursor.callproc("stp_getPageWithPathName", [workflow_id])
                for result1 in cursor.stored_results():
                    columns = [col[0] for col in result1.description]
                    for row in result1.fetchall():
                        page_data.append(dict(zip(columns, row)))
                
            cursor.callproc("stp_geSectionWiseDataForWebsite", [workflow_id])

            for result in cursor.stored_results():
                raw_data = list(result.fetchall())
                columns = [col[0] for col in result.description]

            # Convert each row to a dict
            data_list = [dict(zip(columns, row)) for row in raw_data]

            # Group by 'section_title'
            section_data = defaultdict(list)
            for item in data_list:
                section_title = item.get('section_title')
                if not section_title or not section_title.strip():
                    section_title = 'Others'
                section_data[section_title].append(item)
                
            formatted_data = {}
            for key, val in section_data.items():
                formatted_key = key.replace(" ", "_")  # "Main Slider" -> "Main_Slider"
                formatted_data[formatted_key] = val
            
            if slug == 'Our Product':
                our_products = formatted_data.get('Our_Product', [])
                paginator = Paginator(our_products, 4)  # 4 items per page
                page_obj = paginator.get_page(page_number)

                formatted_data['Our_Product_Paginated'] = page_obj
                formatted_data['current_slug'] = slug
            
            return render(request, page.template_path,
                          {"workflow_data": workflow_data,
                            "section_data": formatted_data,
                            "workflow_id": workflow_id,
                            "page_data": page_data
                          })
        else:
            return render(request, 'Master/Business/BusinessHome.html')
    
    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        cursor.callproc("stp_error_log",[fun,str(e),request.user.id])  
        print(f"error: {e}")
        messages.error(request, 'Oops...! Something went wrong!')
        response = {'result': 'fail','messages ':'something went wrong !'}  
