from django import forms
from django.contrib.auth.models import User
from .models import Address
from django.contrib.auth import authenticate


class RegistrationForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ['username', 'password', 'email']
        help_texts = {'username': None}


class AddressForm(forms.ModelForm):

    class Meta:
        model = Address
        exclude = ['pincode', ]


class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput)

    def clean(self, *args, **kwargs):
        username, password = self.cleaned_data['username'], self.cleaned_data['password']

        user = User.objects.filter(username=username)
        if not user:
            raise forms.ValidationError('Username does not exist')
        else:
            user = authenticate(username=username, password=password)
            if user is None:
                raise forms.ValidationError('Incorrect password for username.')
        return super(LoginForm, self).clean(*args, **kwargs)
