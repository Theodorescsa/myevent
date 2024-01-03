from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.Form):
    last_name = forms.CharField(max_length=100)
    first_name = forms.CharField(max_length=100)
    username = forms.CharField(max_length=100)
    email = forms.EmailField()
    password = forms.CharField(max_length=100, widget=forms.PasswordInput)
    password2 = forms.CharField(max_length=100,widget=forms.PasswordInput)
    
    def clean_password2(self):
        if 'password' in self.cleaned_data:
            password = self.cleaned_data['password']
            password2 = self.cleaned_data['password2']
            
            if password2 and password == password2:
                return password
            raise forms.ValidationError('Passwords do not match')
        
    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            User.objects.get(username=username)
        except User.DoesNotExist:
            return username
        raise forms.ValidationError('Username khong hop le hoac da ton tai')
    def save(self):
        User.objects.create_user(
            last_name = self.cleaned_data['last_name'],
            first_name = self.cleaned_data['first_name'],
            username = self.cleaned_data['username'],
            email = self.cleaned_data['email'],
            password = self.cleaned_data['password'],
        )
    
    
            
    
            