from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.conf import settings
from django.http import HttpResponse, HttpResponseRedirect
from .forms import SeminarForm
from .models import SeminarFormModel, WordDocument
# from django.contrib.auth.models import User
# from django.contrib.auth import get_user_model
from docx import Document
import sqlite3
import os
from django.core.files.base import ContentFile


@login_required(login_url=settings.LOGIN_URL)
def home_page(request):
     main_page=True
     form = SeminarForm(request.POST)
     data = SeminarFormModel.objects.filter(user=request.user)
     return render(request, 'index.html', {'form': form, 'data': data, 'main_page': main_page})

@login_required(login_url=settings.LOGIN_URL)
def seminar_form_req(request):
     submitted=False
     if request.method=='POST':
          form = SeminarForm(request.POST)
          if form.is_valid():
               title = form.cleaned_data['seminar_title']
               speaker = form.cleaned_data['seminar_speaker']
               date = form.cleaned_data['seminar_date']

               seminar_reg = SeminarFormModel.objects.create(
                    user = request.user,
                    seminar_title = title,
                    seminar_speaker = speaker,
                    seminar_date = date
               )

               seminar_reg.save()
               # return render(request, "success.html", {'form': form, 'data': data})
               return HttpResponseRedirect('/add-form?submitted=True')
          # else:   
          #      form = SeminarForm()
          #      message = 'Something went wrong with the submission. Try again.'
          #      return render(request, 'index.html', {'form': form, 'message': message})
     else:
          form = SeminarForm()
          if 'submitted' in request.GET:
               submitted = True
     return render(request, 'index.html', {'form': form, 'submitted': submitted})

def all_seminars(request):
     data = SeminarFormModel.objects.filter(user=request.user)
     return render(request, 'form-list.html',  {'data': data})


def generate_report(request):
     data = SeminarFormModel.objects.filter(user=request.user)
     report_generated=False
     user=request.user
     # Step 1: Connect to SQLite database and retrieve data
     db_path = r"C:\Users\berna\Documents\Coding Projects\Python App\seminar_form\db.sqlite3"  # Path to your SQLite database
     query = "SELECT * FROM web_app_seminarformmodel WHERE user_id="+str(user.id)  # Replace with your query
     conn = sqlite3.connect(db_path)
     cursor = conn.cursor()
     cursor.execute(query)

     # Fetch all rows and column names
     rows = cursor.fetchall()
     columns = [description[0] for description in cursor.description]

     # Close the database connection
     conn.close()
     doc_path=r'C:\Users\berna\Documents\Coding Projects\Python App\seminar_form\media\seminar_declaration.docx'
     document = Document(doc_path)
     num_rows = len(rows) + 1  # +1 for the header row
     num_cols = len(columns)
     table = document.add_table(rows=num_rows, cols=num_cols)

     # Add the header row
     header_row = table.rows[0]
     for idx, column_name in enumerate(columns):
          header_row.cells[idx].text = column_name

     # Add the data rows
     for i, row_data in enumerate(rows, start=1):  # Start from 1 because 0 is the header
          row = table.rows[i]
          for j, cell_data in enumerate(row_data):
               row.cells[j].text = str(cell_data)  # Convert to string if not already

     # Step 4: Save the updated document
     # document.save(f'C:/Users/berna/Documents/Coding Projects/Python App/seminar_form/media/seminar_form_report_{user}.docx')
     # if os.path.exists(f'C:/Users/berna/Documents/Coding Projects/Python App/seminar_form/media/seminar_form_report_{user}.docx'):
     #      report_generated = True
     from io import BytesIO
     buffer = BytesIO()
     document.save(buffer)
     buffer.seek(0)

     # Step 5: Save the file to the Django database
     word_file = WordDocument(name=f"Generated Report {user}")
     word_file.file.save(f"generated_report_{user}.docx", ContentFile(buffer.read()))
     buffer.close()
     return HttpResponse("Word document updated and saved to the database.")
     # else:
     #      report_generated = False
     #      return render(request, 'form-list.html',  {'report_generated': report_generated, 'data': data})



# EXECEPTIONS

def error_403(request, exception):
     return render(request, 'accounts/blocked.html')


def error_404(request, exception):
     return render(request, 'accounts/not-found.html')

def error_500(request):
     return render(request, '500.html', status=500)
