from django.conf.urls import url
from RestService import views

urlpatterns = [
    url(r'module/search', views.search),
    url(r'module/testModule', views.testmodule)
]
