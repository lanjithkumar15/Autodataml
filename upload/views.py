from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage
from linear.views import variselect

def login(request):
    return render(request, 'login.html')

def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'About.html')

def contact(request):
    return render(request, 'Contact.html')

def upload(request):
    if request.method == 'POST' and 'excel_file' in request.FILES:
        excel_file = request.FILES['excel_file']
        
        if excel_file.name.endswith(('.xls', '.xlsx')):
            fs = FileSystemStorage(location='/home/lanjithkumar15/programming/python-django-ml-project/main/media')
            filename = fs.save(excel_file.name, excel_file)
            return redirect('linear:variselect')
    
    return render(request, 'upload.html')

def failure(request):
    return render(request, 'failure.html')
