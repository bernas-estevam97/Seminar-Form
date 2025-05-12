from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'id': 'login-user',
            'onfocus': "this.placeholder=''",
            'onblur': "this.placeholder='Username'"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'id': 'login-password',
            'onfocus': "this.placeholder=''",
            'onblur': "this.placeholder='Password'"
        })
    )

class RegisterForm(forms.Form):
    first_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'First Name',
            'id': 'name',
            'onfocus': "this.placeholder=''",
            'onblur': "this.placeholder='First Name'"
        })
    )
    last_name = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'placeholder': 'Last Name',
            'id': 'name',
            'onfocus': "this.placeholder=''",
            'onblur': "this.placeholder='Last Name'"
        })
    )
    username = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={
            'placeholder': 'Username',
            'id': 'register-user',
            'onfocus': "this.placeholder=''",
            'onblur': "this.placeholder='Username'"
        })
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Password',
            'id': 'signup-password',
            'onfocus': "this.placeholder=''",
            'onblur': "this.placeholder='Password'"
        })
    )
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'placeholder': 'Confirm Password',
            'id': 'confirm_password',
            'onfocus': "this.placeholder=''",
            'onblur': "this.placeholder='Confirm Password'"
        })
    )

    def clean_confirm_password(self):
        # Custom validation to ensure that the password and confirm_password match
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            # Add error to the messages framework
            raise forms.ValidationError("Passwords do not match")
        return confirm_password