"""
URL configuration for passaccess project.

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


# There are 4 already defined handler methods in `django.urls` functions.
handler400 = 'account.views.error_400'
handler403 = 'account.views.error_403'
handler404 = 'account.views.error_404'
handler500 = 'account.views.error_500'


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('account.urls')),
    path('', include('secureapp.urls')),
]
