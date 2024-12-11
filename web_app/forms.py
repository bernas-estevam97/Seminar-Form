from django import forms
from .models import SeminarFormModel
import datetime


class SeminarForm(forms.Form):
    # Semianr title
    seminar_title=forms.CharField(
        max_length = 200,
        label = "Seminar Title",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
    )
    #Speaker name
    seminar_speaker=forms.CharField(
        max_length = 100,
        label = "Seminar Title",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }
        ),
    )
    #seminar date
    seminar_date=forms.DateField(
        widget=forms.DateInput(attrs={
            'class':'form-control',
            'type': 'date'
        }
        ),
        # initial= datetime.date.today(),
    )


# class SeminarForm(forms.ModelForm):
#     class Meta:
#         model = SeminarFormModel
#         fields = '__all__'
#         widgets = {
#             'my_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
#         }
