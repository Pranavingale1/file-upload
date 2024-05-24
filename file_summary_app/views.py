from django.shortcuts import render
from .forms import FileUploadForm
import pandas as pd
import io


def custom_summary_report(df):
    summary = df.describe().to_dict()
    return summary


def upload_file(request):
    if request.method == 'POST':
        form = FileUploadForm(request.POST, request.FILES)
        if form.is_valid():
            uploaded_file = request.FILES['file']

            # Check file extension
            file_extension = uploaded_file.name.split('.')[-1].lower()
            if file_extension == 'csv':
                df = pd.read_csv(io.StringIO(
                    uploaded_file.read().decode('utf-8')))
            elif file_extension in ['xls', 'xlsx']:
                df = pd.read_excel(uploaded_file)
            else:
                return render(request, 'csv_summary_app/error.html', {'message': 'Unsupported file format'})

            summary = custom_summary_report(df)
            return render(request, 'uploadfiles/uploadfile.html', {'summary': summary})
    else:
        form = FileUploadForm()
    return render(request, 'uploadfiles/uploadfile.html', {'form': form})
