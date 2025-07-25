# middleware.py
from django.utils.deprecation import MiddlewareMixin
from workflow.models import *
from workflow.views import *
from django.http import HttpResponseForbidden
import logging

# class ClientDomainRoutingMiddleware(MiddlewareMixin):
#     def process_request(self, request):
#         domain = request.get_host().split(':')[0].lower()  
#         try:
#             # Match domain (e.g., technotest.technowinitinfra.com)
#             client = Client.objects.get(domain_name=domain, is_active=1)
#             request.client = client  # Make available in views/middleware

#             # Attach the client's active workflow (if needed downstream)
#             workflow = WebsiteWorkflow.objects.filter(client_id=client.id, is_active=1).first()
#             request.workflow = workflow
            
#             return dynamic_dispatch(request)
        
#         except Client.DoesNotExist:
#             return HttpResponseNotFound("Client site not found.")
#         except Exception as e:
#             return HttpResponseNotFound(f"Error while loading client workflow: {str(e)}")


# class ClientDomainRoutingMiddleware(MiddlewareMixin):
#     def process_request(self, request):
       
#         domain = request.get_host().split(':')[0].lower()
#         try:
#             client = Client.objects.get(domain_name=domain, is_active=1)
#             request.client = client

#             workflow = WebsiteWorkflow.objects.filter(client_id=client.id, is_active=1).first()
#             request.workflow = workflow

#             return dynamic_dispatch(request)

#         except Client.DoesNotExist:
#             request.client = None
#             request.workflow = None
#             # Just continue processing the request — no redirect, no error
#             return None

#         except Exception as e:
#             # Optional: log this if you need to debug
#             request.client = None
#             request.workflow = None
#             return None  # Also skip hard failure on unexpected exceptions

ALLOWED_DEV_HOSTS = ['3.111.141.151']
class ClientDomainRoutingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        domain = request.get_host().split(':')[0].lower()

        # ✅ Whitelist dev IPs or trusted internal domains
        if domain in ALLOWED_DEV_HOSTS:
            request.client = None
            request.workflow = None
            return None

        try:
            client = Client.objects.get(domain_name=domain, is_active=1)
            request.client = client

            workflow = WebsiteWorkflow.objects.filter(client_id=client.id, is_active=1).first()
            request.workflow = workflow

            return dynamic_dispatch(request)

        except Client.DoesNotExist:
            return HttpResponseForbidden("403 Forbidden: Unauthorized domain")

        except Exception:
            return HttpResponseForbidden("403 Forbidden: Internal error")


