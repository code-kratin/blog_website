from django import forms
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm, UsernameField
from django.contrib.auth.models import User
from django.utils.translation import gettext, gettext_lazy as _
from .models import Blog

class SignUpForm(UserCreationForm):
    password1 = forms.CharField(label="Password", widget=forms.PasswordInput(attrs = {'class':'form-control'}))
    password2 = forms.CharField(label="Confirm Password",widget=forms.PasswordInput(attrs = {'class':'form-control'}))
    class Meta:
        model = User
        fields = ['username','first_name','last_name','email']
        labels = {'first_name': 'First Name','last_name':'Last Name','email':'Email'}
        widgets = {'username':forms.TextInput(attrs={'class':'form-control'}),
                   'first_name':forms.TextInput(attrs={'class':'form-control'}),
                   'last_name':forms.TextInput(attrs={'class':'form-control'}),
                   'email':forms.EmailInput(attrs={'class':'form-control'}),
                   }
        
class LoginForm(AuthenticationForm):
    username = UsernameField(widget = forms.TextInput(attrs = {'class':'form-control'}))
    password = forms.CharField(label=_("Password"),strip = False, widget = forms.PasswordInput(attrs={'class':'form-control'}))


class BlogForm(forms.ModelForm):
    class Meta:
        model = Blog
        fields = ['title','cont']
        labels = {'title':'Title','cont':'Content'}
        widgets = {'title':forms.TextInput(attrs={'class':'form-control'}),'cont':forms.Textarea(attrs={'class':'form-control'})}


class ProfileForm(forms.ModelForm):
    email = forms.EmailField(required=True)  # Ensure email is required
    first_name = forms.CharField(required=True)  # Ensure first name is required
    last_name = forms.CharField(required=True)  # Ensure last name is required
    image = forms.ImageField(required=False)  # Allow optional image update

    class Meta:
        model = User
        fields = ('email', 'first_name', 'last_name', 'image')

    def clean_email(self):
        email = self.cleaned_data['email']
        if User.objects.filter(email=email).exclude(pk=self.instance.pk).exists():
            raise forms.ValidationError('This email address is already in use.')
        return email
    
    
class UpdateUserForm(forms.ModelForm):
    username = forms.CharField(max_length=100,
                               required=True,
                               widget=forms.TextInput(attrs={'class': 'form-control'}))
    first_name = forms.CharField(required=True,  widget=forms.TextInput(attrs={'class': 'form-control'}))  
    last_name = forms.CharField(required=True,  widget=forms.TextInput(attrs={'class': 'form-control'}))  
    email = forms.EmailField(required=True,
                             widget=forms.TextInput(attrs={'class': 'form-control'}))

    class Meta:
        model = User
        fields = ['username','first_name','last_name' ,'email']


class ContactForm(forms.Form):
    name = forms.CharField()
    email = forms.EmailField()
    message = forms.CharField(widget=forms.Textarea)

