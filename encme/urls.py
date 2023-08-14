"""
URL configuration for encme project.

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
from django.urls import path, include
from datetime import datetime
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.mixins import LoginRequiredMixin


class LoginCustom(LoginView):
    def get_context_data(self, **kwargs):
        the_year = datetime.today().year
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            self.redirect_field_name: self.get_redirect_url(),
            'the_year':the_year,
            'site': current_site,
            'site_name': current_site.name,
            **(self.extra_context or {})
        })
        return context
    

class LogoutCustom(LoginRequiredMixin ,LogoutView):
    the_year = datetime.today().year
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        current_site = get_current_site(self.request)
        context.update({
            'the_year': self.the_year,
            'site': current_site,
            'site_name': current_site.name,
            # 'title': _('Logged out'),
            **(self.extra_context or {})
        })
        return context
    
    
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', LoginCustom.as_view(template_name='account/login.html'), name='login'),
    path('logout/', LogoutCustom.as_view(template_name='account/logout.html'), name='logout'),
    path('', include('secureapp.urls')),
]
