from django.views import View
from django.shortcuts import render, HttpResponse, redirect, reverse
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from .forms import RegistrationForm, AddressForm, LoginForm
from .Pincode import get_pincode
from .models import Profile

# Create your views here.

class Login(View):

    def get(self, request, *args, **kwargs):
        form = LoginForm()
        context = {'form':form}
        return render(request, 'accounts/Login.html', context=context)

    def post(self, request, *args, **kwargs):
        form = LoginForm(request.POST)
        if form.is_valid():
            username, password = form.cleaned_data['username'], form.cleaned_data['password']
            user = authenticate(username=username, password=password)
            login(request, user=user)
            return redirect(reverse('displaypin'))
        context = {'form': form}

        return render(request, 'accounts/Login.html', context=context)

class Logout(View):

    def get(self, request, *args,**kwargs):
        logout(request)
        return redirect(reverse('Home'))


class Register(View):


    def get(self, request, *args, **kwargs):
        form = RegistrationForm()
        context = {
            'form': form,
        }
        return render(request, 'accounts/Register.html', context=context)

    def post(self, request, *args, **kwargs):
        form = RegistrationForm(request.POST)
        if form.is_valid():
            new_user = form.save(commit=False)
            password = form.cleaned_data['password']
            new_user.set_password(password)
            new_user.save()
            login(request, new_user)
            return redirect(reverse('address'))
        context = {
            'form': form,
        }
        return render(request, 'accounts/Register.html', context=context)

class Address(LoginRequiredMixin, View):

    def get(self, request, *args, **kwargs):
        form = AddressForm()
        if request.user.profile.address:
            form = AddressForm(instance=request.user.profile.address)
        context = {'form': form}
        return render(request, 'accounts/Address.html', context=context)

    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)
        error_msg = ""
        if form.is_valid():
            data = form.cleaned_data
            address = ",".join((data['locality'], data['city'], data['state'], 'India'))
            pincode = -1
            success = True
            try:
                pincode = get_pincode(address=address)
            except:
                success = False
                error_msg = "Unable to retrieve pincode at the moment. Please try again later."
            else:
                if pincode is None:
                    success = False
                    error_msg = "Can't get pincode for the given address. Please enter a valid address."

            context = {
                'form': form,
                'error_msg': error_msg,
                'pincode': pincode,
            }

            if success:
                prev_address = None
                if request.user.profile.address:
                    prev_address = request.user.profile.address
                address = form.save(commit=False)
                address.pincode = pincode
                address.save()
                profile = Profile.objects.get(user=request.user)
                profile.address = address
                profile.save()
                if prev_address:
                    prev_address.delete()
                return redirect(reverse('displaypin'))
            else:
                return render(request, 'accounts/Address.html', context=context)

        context = {
            'form': form,
            'error_msg': error_msg
        }
        return render(request, 'accounts/Address.html', context=context)

class Home(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/Home.html')


class DisplayPin(View):

    def get(self, request, *args, **kwargs):
        return render(request, 'accounts/DisplayPin.html')