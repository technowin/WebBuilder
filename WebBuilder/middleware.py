# middleware.py
from django.utils.deprecation import MiddlewareMixin
from workflow.models import *
from django.http import HttpResponseNotFound
from workflow.views import *

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


class ClientDomainRoutingMiddleware(MiddlewareMixin):
    def process_request(self, request):
       
        domain = request.get_host().split(':')[0].lower()
        try:
            client = Client.objects.get(domain_name=domain, is_active=1)
            request.client = client

            workflow = WebsiteWorkflow.objects.filter(client_id=client.id, is_active=1).first()
            request.workflow = workflow

            return dynamic_dispatch(request)

        except Client.DoesNotExist:
            request.client = None
            request.workflow = None
            # Just continue processing the request — no redirect, no error
            return None

        except Exception as e:
            # Optional: log this if you need to debug
            request.client = None
            request.workflow = None
            return None  # Also skip hard failure on unexpected exceptions
        
