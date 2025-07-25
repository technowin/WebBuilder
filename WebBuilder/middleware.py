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
        

logger = logging.getLogger(__name__)

class ClientDomainRoutingMiddleware(MiddlewareMixin):
    def process_request(self, request):
        domain = request.get_host().split(':')[0].lower()

        try:
            # Check if the domain exists in the Client table
            client = Client.objects.get(domain_name=domain, is_active=1)
            request.client = client

            # Fetch associated workflow
            workflow = WebsiteWorkflow.objects.filter(client_id=client.id, is_active=1).first()
            request.workflow = workflow

            # Optional: dispatch to a custom view handler
            # return dynamic_dispatch(request)

            # Let the request continue
            return dynamic_dispatch(request)

        except Client.DoesNotExist:
            request.client = None
            request.workflow = None
            logger.warning(f"[ClientDomainRouting] Forbidden access from unknown domain: {domain}")
            return HttpResponseForbidden("403 Forbidden: Unauthorized domain")

        except Exception as e:
            request.client = None
            request.workflow = None
            logger.exception(f"[ClientDomainRouting] Error processing domain {domain}: {str(e)}")
            return HttpResponseForbidden("403 Forbidden: Internal error")

