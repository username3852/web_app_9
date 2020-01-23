"""project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from news import views  # means to import the views from the current folder i.e. project
from django.conf import settings # this is for static
from django.conf.urls.static import static # this is also for the static

urlpatterns = [
    path('admin/', admin.site.urls),
    # path('', views.home, name='home'), # adding the function path 
    path('', views.NewsTemplateView.as_view(), name='home'), # ued because it is landing page 
    path('news/', include('news.urls')), #adding the classbased path of news
    path("accounts/", include("accounts.urls")),
]+ static(settings.STATIC_URL, document_root=settings.STATIC_ROOT) # adding the static path

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
