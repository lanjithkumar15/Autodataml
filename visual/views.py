import pandas as pd
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import UploadForm
from django.core.files.storage import FileSystemStorage
from pathlib import Path
from django.conf import settings
import os
import json

def upload_excel(request):
    if request.method == 'POST':
        form = UploadForm(request.POST, request.FILES)
        if form.is_valid():
            excel_file = request.FILES['excel_file']

            if excel_file.name.endswith(('.xls', '.xlsx','.xl')):
                fs = FileSystemStorage(location='/home/lanjithkumar15/programming/python-django-ml-project/main/media')
                filename = fs.save(excel_file.name, excel_file)
                messages.success(request, 'Excel file uploaded successfully.')

                request.session['uploaded_file_path'] = fs.path(filename)
                return redirect('visual:select_variables')
            else:
                messages.error(request, 'Invalid file format. Please upload an Excel file.')
                return redirect('visual:upload_excel')
        else:
            messages.error(request, 'Form is invalid.')
    else:
        form = UploadForm()

    return render(request, 'upload.html', {'form': form})


def select_variables(request):
    
    file_directory = "/home/lanjithkumar15/programming/python-django-ml-project/main/media"
    excel_files = [file for file in os.listdir(file_directory) if file.endswith((".xlsx", ".xls"))]
    if excel_files:
        first_excel_file = excel_files[0]
        file_path = os.path.join(file_directory, first_excel_file)
        dataframe = pd.read_excel(file_path)
        columns = dataframe.columns.tolist()
        context = {'columns': columns}
        return render(request, 'select_variables.html', context)
    return render(request, 'select_variables.html')

def visualize_data(request):
    if request.method == 'POST':
        variable1 = request.POST.get('variable1')
        variable2 = request.POST.get('variable2')
        chart_type = request.POST.get('chart_type')

        file_directory = '/home/lanjithkumar15/programming/python-django-ml-project/main/media'
        excel_files = [file for file in os.listdir(file_directory) if file.endswith((".xlsx", ".xls"))]
        if excel_files:
            first_excel_file = excel_files[0]
            file_path = os.path.join(file_directory, first_excel_file)
        else:
            file_path = ''  # Provide a default value if no Excel files are found

        dataframe = pd.read_excel(file_path)

        variable1_data = dataframe[variable1].tolist()
        variable2_data = dataframe[variable2].tolist()

        chart_data = {
            'type': chart_type,
            'labels': variable1_data,
            'datasets': [
                {
                    'label': variable2,
                    'data': variable2_data,
                    'fill': False,
                    'borderColor': 'rgb(75, 192, 192)',
                    'backgroundColor': 'rgba(75, 192, 192, 0.2)',
                    'pointBackgroundColor': 'rgb(75, 192, 192)',
                    'pointBorderColor': '#fff',
                    'pointHoverBackgroundColor': '#fff',
                    'pointHoverBorderColor': 'rgb(75, 192, 192)'
                }
            ]
        }

        chart_data_json = json.dumps(chart_data)

        context = {
            'chart_data': chart_data_json,
            'variable1_name': variable1,
            'variable2_name': variable2,
            'chart_color': 'rgb(100, 200, 200)'
        }
        return render(request, 'generate_chart.html', context)
        
    return render(request, 'select_variables.html')