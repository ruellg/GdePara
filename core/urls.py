"""NovikovTT URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.11/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.views.generic.base import TemplateView
from core import views as core_views
from django.conf import settings
from django.conf.urls.static import static
from core.forms import ProfileRegistrationForm, LoginForm
from registration.backends.default.views import RegistrationView
from core.views import LoginView, SignupView
#from registration.backends.default.urls import url, include

urlpatterns = [
    url(r'accounts/register/$', 
            SignupView, 
            name = 'registration_register'),
    url(r'accounts/login/$', 
            LoginView, 
            name = 'auth_login'),

    url(r'^accounts/', include('registration.backends.default.urls')),

    url(r'^$', TemplateView.as_view(template_name='home.html'), name='home'),
    url(r'^index/$', core_views.index, name='index'),
    url(r'^profile/$', core_views.profile_read, name='profile'),
    url(r'^admin/', admin.site.urls),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
