"""Cookit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.9/topics/http/urls/
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
from django.conf.urls import url

from NLU import views

urlpatterns = [
    # url(r'^admin/', admin.site.urls),
    url(r'^$', views.redirect2main, name='redirect'),
    url(r'^home/$', views.home, name='home'),
    url(r'^checklogin/$', views.check_login, name='checkLogin'),

    url(r'^download/$', views.download, name='download'),
    url(r'^data/$', views.get_data, name='data'),

    url(r'^wseg/$', views.word_segment, name='wordSegment'),
    url(r'^mtest/$', views.model_test, name='modelTest'),


]
