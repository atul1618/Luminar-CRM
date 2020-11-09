from django import forms
from django.contrib.auth.models import  User
from django.contrib.auth.forms import UserCreationForm

class UserRegForm(UserCreationForm):
    class Meta:
        model=User
        fields = ['first_name', 'last_name', 'username', 'email', 'password1', 'password2']
        widgets = {
            'first_name': forms.TextInput(attrs={'placeholder': 'First Name'}),
            'last_name': forms.TextInput(attrs={'placeholder': 'Last Name'}),
            'username': forms.TextInput(attrs={'placeholder': 'Username'}),
            'email': forms.EmailInput(attrs={'placeholder': 'Email Address'}),
        }

    def __init__(self, *args, **kwargs):
        super(UserRegForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'placeholder': 'Enter Your Password'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'placeholder': 'Confirm Password'})

    def clean(self):
        print("inside clean")
        cleaned_data = super().clean()
        userid = cleaned_data.get('username')
        mail = cleaned_data.get('email')
        pwd1 = cleaned_data.get('password1')
        pwd2 = cleaned_data.get('password2')
        print("Username:", userid)
        print("Email:", mail)
        print("Password 1:", pwd1)
        print("Password 2:", pwd2)
        qs = User.objects.filter(username=userid)
        if qs:
            print("Username exists")
            msg = "Username exists"
            self.add_error('username', msg)
        else:
            print("Username created")
        import re
        rule = '[a-z0-9_.]*@[a-z]*.com'
        match = re.fullmatch(rule, mail)
        if match == None:
            msg = "Invalid email address"
            self.add_error('email', msg)
            print("Invalid")
        else:
            print(" Email Valid")
        qs1 = User.objects.filter(email=mail)
        if qs1:
            print("Email already registered")
            msg = "Email address already registered"
            self.add_error('email', msg)

