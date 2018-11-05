from django.conf.urls import url
from django.urls import path

from .views import dashboard,macfilter,module,network,password,reboot,systemlog

urlpatterns =[
    url(r'dashboard', dashboard),
    url(r'macfilter', macfilter),
    url(r'module', module),
    url(r'network', network),
    url(r'password', password),
    url(r'reboot', reboot),
    url(r'systemlog', systemlog)
]
