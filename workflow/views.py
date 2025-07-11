from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib import messages
from django.db import connection
import traceback
import Db 
from workflow.models import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from workflow.models import *
from django.urls import reverse
from django.conf import settings
import os
from django.core.files.storage import FileSystemStorage
import time
from .models import WebsiteWorkflow
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.core.exceptions import ObjectDoesNotExist
from WebBuilder.encryption import encrypt_parameter
from django.core.mail import send_mail

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
        if request.method == 'GET':
            username = request.session.get("username", "")
            workflows = WebsiteWorkflow.objects.select_related('template', 'category').filter(
                created_by=username
            )
            return render(request, 'Workflow/MySites.html', {'workflows': workflows})

        if request.method == 'POST':
            print("POST request received in mySites")

            username = request.session.get("username", "")
            workflow_id = request.POST.get("workflow_id")

            website_name = request.POST.get("website_name", "").strip()
            primary_color = request.POST.get("primary_color", "").strip()
            secondary_color = request.POST.get("secondary_color", "").strip()

            facebook_url = request.POST.get("facebook_url", "").strip()
            instagram_url = request.POST.get("instagram_url", "").strip()
            youtube_url = request.POST.get("youtube_url", "").strip()
            linkedin_url = request.POST.get("linkedin_url", "").strip()

            # New Fields
            address = request.POST.get("address", "").strip()
            phone = request.POST.get("phone", "").strip()
            email = request.POST.get("email", "").strip()

            enable_accessibility = 1 if request.POST.get("enable_accessibility") == "on" else 0
            show_second_logo = 1 if request.POST.get("show_second_logo") == "on" else 0

            logo = request.FILES.get("logo")
            favicon = request.FILES.get("favicon")
            second_logo = request.FILES.get("second_logo")

            MAX_FILE_SIZE_MB = 5
            MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024

            def save_file(file_obj, workflow_id, subfolder):
                if not file_obj:
                    return None

                if file_obj.size > MAX_FILE_SIZE:
                    raise ValueError(f"{file_obj.name} exceeds {MAX_FILE_SIZE_MB} MB.")

                folder_path = os.path.join(settings.MEDIA_ROOT, str(workflow_id), subfolder)
                os.makedirs(folder_path, exist_ok=True)

                fs = FileSystemStorage(location=folder_path)
                original_name, ext = os.path.splitext(file_obj.name)
                safe_name = "".join(c for c in original_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                timestamp = time.strftime('%Y%m%d_%H%M%S')
                final_name = f"{safe_name}_{timestamp}{ext}"

                filename = fs.save(final_name, file_obj)
                return os.path.join(str(workflow_id), subfolder, filename).replace('\\', '/')

            if not workflow_id:
                # Create new
                workflow = WebsiteWorkflow.objects.create(
                    website_name=website_name or None,
                    primary_color=primary_color or None,
                    secondary_color=secondary_color or None,
                    facebook_url=facebook_url or None,
                    instagram_url=instagram_url or None,
                    youtube_url=youtube_url or None,
                    linkedin_url=linkedin_url or None,
                    address=address or None,
                    phone_number=phone or None,
                    email_address=email or None,
                    enable_accessibility=enable_accessibility,
                    show_second_logo=show_second_logo,
                    created_at=timezone.now(),
                    created_by=username
                )

                if logo:
                    workflow.logo = save_file(logo, workflow.id, "Image")
                if favicon:
                    workflow.favicon = save_file(favicon, workflow.id, "Favicon")
                if second_logo:
                    workflow.second_logo = save_file(second_logo, workflow.id, "Second Logo")

                workflow.save()
                messages.success(request, "New branding created successfully!")

            else:
                # Update existing
                workflow = WebsiteWorkflow.objects.filter(id=workflow_id).first()
                if not workflow:
                    messages.error(request, "Workflow not found for update.")
                    return redirect('mySites')

                workflow.website_name = website_name or workflow.website_name
                workflow.primary_color = primary_color or workflow.primary_color
                workflow.secondary_color = secondary_color or workflow.secondary_color
                workflow.facebook_url = facebook_url or workflow.facebook_url
                workflow.instagram_url = instagram_url or workflow.instagram_url
                workflow.youtube_url = youtube_url or workflow.youtube_url
                workflow.linkedin_url = linkedin_url or workflow.linkedin_url
                workflow.address = address or workflow.address
                workflow.phone_number = phone or workflow.phone_number
                workflow.email_address = email or workflow.email_address
                workflow.enable_accessibility = enable_accessibility
                workflow.show_second_logo = show_second_logo

                if logo:
                    workflow.logo = save_file(logo, workflow_id, "Image")
                if favicon:
                    workflow.favicon = save_file(favicon, workflow_id, "Favicon")
                if second_logo:
                    workflow.second_logo = save_file(second_logo, workflow.id, "Second Logo")

                workflow.updated_at = timezone.now()
                workflow.updated_by = username
                workflow.save()

                messages.success(request, "Branding updated successfully!")

            return redirect('mySites')

        
    except Exception as e:
        import traceback
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        user_id = getattr(request.user, 'id', None)
        if user_id:
            cursor.callproc("stp_error_log", [fun, str(e), user_id])
        print(f"Error: {e}")
        messages.error(request, "Oops! Something went wrong.")
        return redirect('mySites')

@login_required
def startEditing(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor = m.cursor(dictionary=True)  # so results are dicts, not tuples

    try:
        workflow_id = request.GET.get('workflow_id')

        # Call stored procedure
        cursor.callproc("stp_getPagesSection", [workflow_id])

        # MySQL returns result sets in cursor.stored_results()
        for result in cursor.stored_results():
            rows = result.fetchall()

        # Process results to group sections under pages
        from collections import defaultdict
        page_map = defaultdict(list)
        page_titles = {}

        for row in rows:
            page_id = row['page_id']
            page_titles[page_id] = row['page_title']
            page_map[page_id].append(row)

        pages_with_sections = [
            {
                'page_id': page_id,
                'page_title': page_titles[page_id],
                'sections': sections
            }
            for page_id, sections in page_map.items()
        ]

        return render(request, 'Workflow/StartEditing.html', {
            'workflow_id': workflow_id,
            'pages': pages_with_sections
        })

    except Exception as e:
        import traceback
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        request.user.id and cursor.callproc("stp_error_log", [fun, str(e), request.user.id])
        print(f"Error: {e}")
        messages.error(request, "Oops! Something went wrong.")
        return redirect('startEditing')

@login_required
def submitEditing(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor = m.cursor()

    try:
        username = request.session.get("username", "")
        title = request.POST.get('title') or ''
        description = request.POST.get('description') or ''
        workflow_id = request.POST.get('workflow_id')
        page_id = request.POST.get('page_id')
        section_id = request.POST.get('section_id')
        uploaded_file = request.FILES.get('media_file', None)

        # At least one of these fields is required
        if not (title or description or uploaded_file):
            messages.error(request, "Please provide at least Title, Description or File.")
            return redirect(f"/startEditing?workflow_id={workflow_id}")

        saved_path = None

        if uploaded_file:
            # ✅ File size validation
            MAX_FILE_SIZE_MB = 5
            MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024  # 5 MB in bytes

            if uploaded_file.size > MAX_FILE_SIZE:
                messages.error(request, f"File size should not exceed {MAX_FILE_SIZE_MB} MB.")
                return redirect(f"/startEditing?workflow_id={workflow_id}")

            # 📁 Save file
            folder_path = os.path.join(settings.MEDIA_ROOT, str(workflow_id), str(page_id), str(section_id))
            os.makedirs(folder_path, exist_ok=True)

            fs = FileSystemStorage(location=folder_path)

            import time
            original_name = os.path.splitext(uploaded_file.name)[0]
            ext = os.path.splitext(uploaded_file.name)[1]

            # Sanitize filename (optional but recommended)
            safe_name = "".join(c for c in original_name if c.isalnum() or c in (' ', '-', '_')).rstrip()

            # Add timestamp to filename
            timestamp = time.strftime('%Y%m%d_%H%M%S')
            final_name = f"{safe_name}_{timestamp}{ext}"

            filename = fs.save(final_name, uploaded_file)

            saved_path = os.path.join(str(workflow_id), str(page_id), str(section_id), filename).replace('\\', '/')

        # ✅ Create DB entry
        section_instance = Section.objects.get(id=section_id)
        ContentBlock.objects.create(
            section=section_instance,
            title=title,
            description=description,
            block_type='file' if uploaded_file else 'text',
            media_file=saved_path,
            created_by=username,
            created_at=timezone.now()
        )

        messages.success(request, "Content saved successfully.")
        return redirect(f"/startEditing?workflow_id={workflow_id}")

    except Exception as e:
        import traceback
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        if request.user.id:
            cursor.callproc("stp_error_log", [fun, str(e), request.user.id])
        print(f"Error: {e}")
        messages.error(request, "Oops! Something went wrong.")
        return redirect(f"/startEditing?workflow_id={workflow_id}")

@login_required
@require_POST
def renameSiteDetails(request):
    # Optional: close old connections if you're handling raw DB manually
    Db.closeConnection()
    m = Db.get_connection()
    cursor = m.cursor()

    try:
        workflow_id = request.POST.get('workflow_id')

        if not workflow_id:
            return JsonResponse({'error': 'Workflow ID is required'}, status=400)

        try:
            workflow = WebsiteWorkflow.objects.get(id=workflow_id)
        except ObjectDoesNotExist:
            return JsonResponse({'error': 'WebsiteWorkflow not found'}, status=404)

        response_data = {
            'workflow_id': workflow.id,
            'website_name': workflow.website_name,
            'primary_color': workflow.primary_color,
            'secondary_color': workflow.secondary_color,
            'facebook_url': workflow.facebook_url,
            'instagram_url': workflow.instagram_url,
            'youtube_url': workflow.youtube_url,
            'linkedin_url': workflow.linkedin_url,
            'enable_accessibility': workflow.enable_accessibility,
            'show_second_logo': workflow.show_second_logo,
            'address': workflow.address,
            'phone_number': workflow.phone_number,
            'email_address': workflow.email_address,
        }
        return JsonResponse(response_data)

    except Exception as e:
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        if request.user.id:
            cursor.callproc("stp_error_log", [fun, str(e), request.user.id])
        print(f"Error: {e}")
        return JsonResponse({'error': 'Something went wrong on the server.'}, status=500)
    
@login_required
def view_document(request):
    if request.method == "POST":
        workflow_id = request.POST.get("workflow_id")
        doc_type = request.POST.get("doc_type")  # 'logo' or 'favicon'

        try:
            workflow = WebsiteWorkflow.objects.get(pk=workflow_id)

            if doc_type == 'logo':
                file_field = workflow.logo
            elif doc_type == 'favicon':
                file_field = workflow.favicon
            elif doc_type == 'second_logo':
                file_field = workflow.second_logo
            else:
                return JsonResponse({'error': 'Invalid document type.'}, status=400)

            if file_field and file_field.name:
                return JsonResponse({
                    'file_url': os.path.join(settings.MEDIA_URL, file_field.name)
                }, status=200)
            else:
                return JsonResponse({'error': 'File not uploaded.'}, status=404)

        except WebsiteWorkflow.DoesNotExist:
            return JsonResponse({'error': 'Workflow not found.'}, status=404)

    return JsonResponse({'error': 'Invalid request method.'}, status=400)

@login_required
def view_index(request):
    Db.closeConnection()
    m = Db.get_connection()
    cursor = m.cursor(dictionary=True)  # so results are dicts, not tuples

    try:
        section_id = request.GET.get('section_id')
        workflow_Id = request.GET.get('workflow_id')
        cursor.callproc("stp_getIndexPage", [section_id])
        for result in cursor.stored_results():
            # rows = result.fetchall()
            index_data = list(result.fetchall())
        
        return render(request, 'Workflow/view_index.html', {"index_data": index_data,"workflow_Id":workflow_Id,"section_id":section_id,
        })

    except Exception as e:
        import traceback
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        request.user.id and cursor.callproc("stp_error_log", [fun, str(e), request.user.id])
        print(f"Error: {e}")
        messages.error(request, "Oops! Something went wrong.")
        return redirect('view_index')
    
@login_required    
def viewEdit_index(request, id, workflow_id):
    Db.closeConnection()
    m = Db.get_connection()
    cursor = m.cursor() 

    try:
        username = request.session.get("username", "")
        if request.method == "GET":
            param =[id]
        # workflow_Id = request.GET.get('workflow_id')
            cursor.callproc("stp_getEditIndexPage", param)
            for result in cursor.stored_results():
                # rows = result.fetchall()
                # data_row = list(result.fetchall())[0]
                data_row = result.fetchall()[0]
                
            context = {
               
                "id": data_row[0],"block_type": data_row[1],"description": data_row[2],"media_file": data_row[3],"section_id": data_row[9],"title": data_row[10],
                "status": data_row[11],"workflow_id":workflow_id,
            }
                
            return render(request, 'Workflow/viewEdit_index.html', context)
        
        if request.method == "POST":
            username = request.session.get("username", "")
            
            # Get page & section id using content id
            paramp = [id]
            cursor.callproc("stp_getEditSecPgId", paramp)
            for result in cursor.stored_results():
                data_ids = result.fetchall()[0]
            page_id = data_ids[2]
            section_id = data_ids[1]

            # Get form data
            title = request.POST.get('title') or ''
            description = request.POST.get('description') or ''
            workflow_id = request.POST.get('workflow_id')
            # page_id = request.POST.get('page_id')
            # section_id = request.POST.get('section_id')
            uploaded_file = request.FILES.get('media_file', None)
            status = 1 if request.POST.get('title_status') == 'on' else 0

            # Require at least one input
            if not (title or description or uploaded_file):
                messages.error(request, "Please provide at least Title, Description or File.")
                return redirect(f"/startEditing?workflow_id={workflow_id}")

            saved_path = None

            if uploaded_file:
                MAX_FILE_SIZE_MB = 5
                MAX_FILE_SIZE = MAX_FILE_SIZE_MB * 1024 * 1024

                if uploaded_file.size > MAX_FILE_SIZE:
                    messages.error(request, f"File size should not exceed {MAX_FILE_SIZE_MB} MB.")
                    return redirect(f"/startEditing?workflow_id={workflow_id}")

                # Save uploaded file
                folder_path = os.path.join(settings.MEDIA_ROOT, str(workflow_id), str(page_id), str(section_id))
                os.makedirs(folder_path, exist_ok=True)

                fs = FileSystemStorage(location=folder_path)
                import time

                original_name = os.path.splitext(uploaded_file.name)[0]
                ext = os.path.splitext(uploaded_file.name)[1]
                safe_name = "".join(c for c in original_name if c.isalnum() or c in (' ', '-', '_')).rstrip()
                timestamp = time.strftime('%Y%m%d_%H%M%S')
                final_name = f"{safe_name}_{timestamp}{ext}"

                filename = fs.save(final_name, uploaded_file)
                saved_path = os.path.join(str(workflow_id), str(page_id), str(section_id), filename).replace('\\', '/')

            # ✅ Call the combined stored procedure
            
            cursor.callproc("stp_UpdateIndexCntentBlock", [title,description,id , saved_path,status])
            m.commit()

            messages.success(request, "Content updated successfully.")
            return redirect(f"/view_index?workflow_id={workflow_id}&section_id={section_id}")

        

    except Exception as e:
        import traceback
        tb = traceback.extract_tb(e.__traceback__)
        fun = tb[0].name
        request.user.id and cursor.callproc("stp_error_log", [fun, str(e), request.user.id])
        print(f"Error: {e}")
        messages.error(request, "Oops! Something went wrong.")
        return redirect("view_index")
    