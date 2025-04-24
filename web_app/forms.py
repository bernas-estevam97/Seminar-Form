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
        widget=forms.TextInput(attrs={
            'class': 'form-control flatpickr w-30 mx-auto',  # Apply custom class for styling
            'placeholder': 'Select a date',  # Add a placeholder for better UX
            'autocomplete': 'off',
        }
        ),
        # initial= datetime.date.today(),
    )
    #verification_code
    verification_code=forms.CharField(
        max_length = 100,
        label = "Verification code",
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control w-30 mx-auto'
        }
        ),
    )


# class SeminarForm(forms.ModelForm):
#     class Meta:
#         model = SeminarFormModel
#         fields = '__all__'
#         widgets = {
#             'my_date': forms.DateInput(format='%Y-%m-%d', attrs={'type': 'date'})
#         }
