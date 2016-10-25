from django import forms

class LoginForm(forms.Form):
	username = forms.CharField(required=True)
	password = forms.CharField(required=True, widget=forms.PasswordInput)

class JobForm(forms.Form):
	name = forms.CharField(required=True)
	description = forms.CharField(widget=forms.Textarea)
	price = forms.IntegerField(required=True)
	location = forms.CharField(required=True)


