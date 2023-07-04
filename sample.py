def visualize_data(request):
    if request.method == 'POST':
        variable1 = request.POST.get('variable1')
        variable2 = request.POST.get('variable2')
        chart_type = request.POST.get('chart_type')

        directory_path = '/home/lanjithkumar15/programming/python-django-ml-project/main/visual/media'
        excel_files = [file for file in os.listdir(directory_path) if file.endswith(('.xl', '.xls', '.xlsx'))]

        if excel_files:
            file_path = os.path.join(directory_path, excel_files[0])
            dataframe = pd.read_excel(file_path)

            variable1_data = dataframe[variable1]
            variable2_data = dataframe[variable2]

            if chart_type == 'line':
                chart = sns.lineplot(x=variable1_data, y=variable2_data)
            elif chart_type == 'bar':
                chart = sns.barplot(x=variable1_data, y=variable2_data)
            elif chart_type == 'pie':
                chart_data = dataframe[variable1].value_counts()
                chart_labels = chart_data.index.tolist()
                chart_values = chart_data.values.tolist()
                plt.pie(chart_values, labels=chart_labels, autopct='%.0f%%')
                chart = plt.gca()
            elif chart_type == 'scatter':
                chart = sns.scatterplot(x=variable1_data, y=variable2_data)

            if chart is not None:
                buffer = io.BytesIO()
                chart.figure.savefig(buffer, format='png')
                plt.close(chart.figure)
                buffer.seek(0)

                chart_image_base64 = base64.b64encode(buffer.getvalue()).decode()

                context = {'chart_image_base64': chart_image_base64}
                return render(request, 'generate_chart.html', context)

    directory_path = '/home/lanjithkumar15/programming/python-django-ml-project/main/visual/media'
    excel_files = [file for file in os.listdir(directory_path) if file.endswith(('.xl', '.xls', '.xlsx'))]

    if excel_files:
        file_path = os.path.join(directory_path, excel_files[0])
        dataframe = pd.read_excel(file_path)
        columns = dataframe.columns.tolist()
    else:
        columns = []

    context = {'columns': columns}
    return render(request, 'select_variables.html', context)
