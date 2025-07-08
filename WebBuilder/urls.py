"""
URL configuration for WebBuilder project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path,include
from django.conf import settings
from django.conf.urls.static import static
from django.views import defaults as default_views
from django.views.generic import TemplateView
from Account.views import *
from workflow.views import *
from Master.views import *

urlpatterns = [
    
    
    path('admin/', admin.site.urls),
    
    # bootstap internal urls
    
    path("apps/", include("bootstrap.apps.urls", namespace="apps")),
    path("apps/crm/", include("bootstrap.crm.urls", namespace="crm")),
    path("apps/ecommerce/", include("bootstrap.ecommerce.urls", namespace="ecommerce")),
    path("pages/", include("bootstrap.pages.urls", namespace="pages")),
    path("ui/", include("bootstrap.ui.urls", namespace="ui")),
    path("extended/", include("bootstrap.extended.urls", namespace="extended")),
    path("icons/", include("bootstrap.icons.urls", namespace="icons")),
    path("charts/", include("bootstrap.charts.urls", namespace="charts")),
    path("forms/", include("bootstrap.form.urls", namespace="form")),
    path("tables/", include("bootstrap.tables.urls", namespace="tables")),
    path("maps/", include("bootstrap.maps.urls", namespace="maps")),
    path("layouts/", include("bootstrap.layouts.urls", namespace="layouts")),
    path("dashboard/", include("bootstrap.dashboard.urls", namespace="dashboard")),
    path("landing", view=TemplateView.as_view(template_name="bootstrap/landing.html"), name="landing"),
    
    # Account
    path("", Login,name='Account'),
    path("Login", Login,name='Account'),
    path("Login", Login,name='Login'),
    path("logout",logoutView,name='logout'),
    
    # Master
    path("businessHome", businessHome,name='businessHome'),
    path("AboutUs", aboutUs,name='aboutUs'),
    path("BusinessContactUs", BusinessContactUs,name='BusinessContactUs'),
    path("Service", servicepage,name='servicepage'),
    
    # Workflow
    path("workflow_starts", workflow_starts,name='workflow_starts'),
    path("GettingStarted", GettingStarted,name='GettingStarted'),
    path("viewTemplate", viewTemplate,name='viewTemplate'),
    path("mySites", mySites,name='mySites'),
    path("startEditing", startEditing,name='startEditing'),
    path("submitEditing", submitEditing,name='submitEditing'),
    path("view_index", view_index,name='view_index')
]

    path("submitEditing", submitEditing,name='submitEditing'),
    path("renameSiteDetails", renameSiteDetails,name='renameSiteDetails'),
    path("view_document", view_document,name='view_document')

    
]   
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)