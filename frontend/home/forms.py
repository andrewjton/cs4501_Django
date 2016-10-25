from django import forms

from .models import Job

class JobForm(forms.ModelForm):

    class Meta:
        model = Job
        fields = ('name', 'location', 'price', 'description',)
        
    class RegisterForm(forms.Form):
        first_name = forms.CharField(required=True)
        last_name = forms.CharField(required=True)
        username = forms.CharField(required=True)
        password = forms.CharField(required=True, widget=forms.PasswordInput)