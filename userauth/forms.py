from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from userauth.models import User
from django.contrib.auth import authenticate

class UserRegisterForm(UserCreationForm):
    username = forms.CharField(widget=forms.TextInput(attrs={"placeholder":"Username"}))
    email = forms.EmailField(widget=forms.EmailInput(attrs={"placeholder":"Email"}))
    password1 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Password"}))
    password2 = forms.CharField(widget=forms.PasswordInput(attrs={"placeholder":"Confirm Password"}))
    
    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
    
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError("This email is already in use.")
        return email




class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['profile_photo', 'full_name', 'employee', 'about_me', 'university_name', 'major']

    def __init__(self, *args, **kwargs):
        super(UserProfileForm, self).__init__(*args, **kwargs)
        self.fields['profile_photo'].widget.attrs['class'] = 'form-control-file'
        self.fields['full_name'].widget.attrs['class'] = 'form-control'
        self.fields['employee'].widget.attrs['class'] = 'form-check-input'
        self.fields['about_me'].widget.attrs['class'] = 'form-control'
        self.fields['university_name'].widget.attrs['class'] = 'form-control'
        self.fields['major'].widget.attrs['class'] = 'form-control'


    

