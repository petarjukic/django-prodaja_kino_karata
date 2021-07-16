from django.forms import ModelForm
from .models import Ticket, Projection, Person
from django.contrib.auth.forms import UserCreationForm
from django import forms
from django.contrib.auth import authenticate 


class TicketForm(ModelForm):
    class Meta:
        model = Ticket
        fields = ('seatNumber', 'projection', 'user')


class RegistrationForm(UserCreationForm):
    email = forms.EmailField(max_length=50, help_text='Required')
    class Meta:
        model = Person
        fields = ("email", "username", "password1", "password2")


class PersonAuthenticateForm(forms.ModelForm):
    password = forms.CharField(label='Password', widget=forms.PasswordInput)
    class Meta:
        model = Person
        fields = ('email', 'password')

    def clean(self):
        if self.is_valid:
            email = self.cleaned_data.get['email']
            password = self.cleaned_data.get['password']
            if not authenticate(email=email, password=password):
                raise forms.ValidationError("Invalid login")
                                        

class SuperUserForm(ModelForm):
    class Meta:
        model = Person
        fields = ('is_admin', 'is_staff', 'is_superuser', 'username')


class ProjectionForm(ModelForm):
    class Meta:
        model = Projection
        fields = ('filmName', 'duration', 'capacity', 'price') 

