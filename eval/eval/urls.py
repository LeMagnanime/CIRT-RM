"""
URL configuration for eval project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
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
from django.urls import path, include
from django.views.generic.base import TemplateView
from evalCIRT import views
from eval import settings
from django.conf.urls.static import static
from evalCIRT.views import analyse
from evalCIRT.views import serve_flask_app




urlpatterns = [
    path('admin/', admin.site.urls),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("", TemplateView.as_view(template_name="home.html"), name="home"),
    path("dashboard/", TemplateView.as_view(template_name="dashboard.html"), name="dashboard"),
    path('ancien_projet/',views.ancien_projet, name="ancien_projet"),
    path('nouveau_projet/', views.nouveau_projet, name="nouveau_projet"),
    path('analyse_quantitative/', views.analyse_quantitative, name='analyse_quantitative'),
    path('analyse_qualitative/', views.analyse_qualitative, name='analyse_qualitative'),
    path('referentiel/',views.referentiel, name='referentiel'),
    path('analyse/', views.analyse, name='analyse'),
    path('analyse/<str:document_name>/', views.analyse, name='analyse_document'),
    path('documents/<int:document_id>/', views.document_view, name='document_view'),


    path('index/', views.index, name='index'),
    path('serve_flask_app/', serve_flask_app, name='serve_flask_app'),
    path('', views.index, name='index'),
    path('index/', TemplateView.as_view(template_name="index.html"), name='index'),
    path('', include('analyse_risques.urls')),
    path('add_actif/', views.add_actif, name='add_actif'),




]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
