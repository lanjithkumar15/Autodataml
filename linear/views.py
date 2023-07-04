import os
import pandas as pd
import matplotlib.pyplot as plt
import base64
from io import BytesIO
from sklearn.linear_model import LinearRegression
from django.shortcuts import render, redirect
from django.core.files.storage import FileSystemStorage

def variselect(request):
    file_directory = "/home/lanjithkumar15/programming/python-django-ml-project/main/media"
    os.chdir(file_directory)
    excel_files = [file for file in os.listdir() if file.endswith((".xlsx", ".xls", ".xl"))]

    if excel_files:
        first_excel_file = excel_files[0]
        file_path = os.path.join(file_directory, first_excel_file)
        df = pd.read_excel(file_path)
        column_names = df.columns.tolist()

        if request.method == 'POST':
            dependent_variable = request.POST.get('dependent_variable')
            independent_variables = request.POST.getlist('independent_variables')
            regression_type = request.POST.get('regression_type')

            X = df[independent_variables]
            y = df[dependent_variable]

            if len(independent_variables) > 1:
                model = LinearRegression()
                regression_type = 'Multiple Linear Regression'
            else:
                model = LinearRegression()
                regression_type = 'Simple Linear Regression'

            model.fit(X, y)
            y_pred = model.predict(X)

            plt.scatter(y_pred, y, color='blue')  # Plot y_pred against y
            plt.plot(y, y, color='red', linewidth=2)  # Plot the ideal line y=y
            plt.xlabel('Predicted Values')
            plt.ylabel('Actual Values')
            plt.title(regression_type)

            plot_buffer = BytesIO()
            plt.savefig(plot_buffer, format='png')
            plot_buffer.seek(0)
            plot_image = base64.b64encode(plot_buffer.getvalue()).decode('utf-8')

            coefficients = model.coef_
            intercept = model.intercept_

            data = {
                'file_name': first_excel_file,
                'columns': independent_variables + [dependent_variable],
                'regression_type': regression_type,
                'coefficients': coefficients.flatten(),
                'intercept': intercept.flatten(),
                'predictions': y_pred.flatten(),
                'plot_image': plot_image,
            }

            return render(request, 'result.html', {'data': [data]})

        context = {
            'column_names': column_names,
        }
        return render(request, 'variable_select.html', context)

    return render(request, 'result.html', {'data': []})
