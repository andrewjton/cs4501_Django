from django import forms
import datetime
from django.utils import timezone
class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput)

class RegisterForm(forms.Form):
	username = forms.CharField(required=False)
	password = forms.CharField(required=True, widget=forms.PasswordInput)
	first_name = forms.CharField(required=True)
	last_name = forms.CharField(required=True)
	date_of_birth = forms.DateField(required=True, initial=timezone.now())
