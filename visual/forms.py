from django import forms

class UploadForm(forms.Form):
    excel_file = forms.FileField(label='Select Excel File')

    # Additional form fields can be added here

    # Optional: Define form field attributes and validation rules
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['excel_file'].widget.attrs.update({'class': 'custom-file-input'})