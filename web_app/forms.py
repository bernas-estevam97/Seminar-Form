from django import forms
from .models import SeminarForm
import datetime


class SeminarForm(forms.ModelForm):
    # Semianr title
    seminar_title=forms.CharField(
        max_length = 50,
        label = "Seminar Title"
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        initial="Seminar title...",
    )
    #Speaker name
    seminar_speaker=forms.CharField(
        max_length = 50,
        label = "Seminar Title"
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control'
        }),
        initial="Speaker name...",
    )
    #seminar date
    seminar_date=forms.DateInput(
        widget=forms.DateInput(
        attrs={
            'class':'form-control'
            'type': 'date'
        }),
        initial=datetime.date.today()
    )


# class SeminarForm(forms.ModelForm):
#     class Meta:
#         model = SeminarFormModel
#         fields = '__all__'
#         widgets = {
#             'my_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
#         }
