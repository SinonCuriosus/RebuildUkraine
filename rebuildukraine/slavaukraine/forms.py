from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate
from django.forms import DateInput

from .models import Person
from .models import Enterprise

class PersonRegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=60, help_text="Required. Add a valid email address.")

    class Meta:
        model = Person
        fields= ("email","username","first_name","last_name","birth", "profile_image", "gender","birth", "address","password1","password2")
        widgets= {'birth': forms.DateInput(
            format=('%Y-%m-%d'),
            attrs={'class': 'form-control',
                   'placeholder': 'Select a date',
                   'type': 'date',
        }),}

class PersonAuthenticationForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)

    class Meta:
        model = Person
        fields = ('email','password')

    def clean(self):
        if self.is_valid():
            email = self.cleaned_data['email']
            password = self.cleaned_data['password']

            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid credentials.");



