"""
URL configuration for CognitiveTestsApp project.

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
from django.urls import path
from landingpage import views as landingpage
from perceptiontest import views as perceptiontest
urlpatterns = [
    path('admin/', admin.site.urls),
    path('', landingpage.index, name="home"),
    path('perceptiontest/', perceptiontest.perceptiontest_form, name="perceptiontest"),
    path('perceptiontest-start/', perceptiontest.image_canvas, name="perceptiontest-start" )
]
