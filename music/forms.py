from django.contrib.auth.models import User
from django import forms


class UserForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput)

    class Meta:  # INFORMACIJE O SAMOJ KLASI U KOJOJ SE NALAZI
        model = User
        fields = ['username', 'email', 'password']
