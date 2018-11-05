from django.shortcuts import render

# Create your views here.

def dashboard(request):
    return render(request, "configure/dashboard.html")

def macfilter(request):
    return render(request, "configure/macfilter.html")

def module(request):
    return render(request, "configure/module.html")

def network(request):
    return render(request, "configure/network.html")

def password(request):
    return render(request, "configure/password.html")

def reboot(request):
    return render(request, "configure/reboot.html")

def systemlog(request):
    return render(request, "configure/systemlog.html")