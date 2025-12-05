from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

def custom_permission_denied(request, exception):
    return render(request, '403.html', status=403)