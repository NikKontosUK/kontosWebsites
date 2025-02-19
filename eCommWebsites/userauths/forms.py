from django import forms
from django.contrib.auth.forms import UserCreationForm
from userauths.models import User

class UserRegisterForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={"placeholder": "Email"})
    )    
    phone_number = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Phone"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password Confirmation"}))

    class Meta:
        model = User
        fields = ['email', 'phone_number','password1','password2']