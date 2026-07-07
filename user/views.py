from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin
from django.shortcuts import render, redirect
from django.views import View
from django.contrib.auth.models import User
import re

from order.models import Order


class LoginView(View):
    template_name = 'auth/login.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('profile')
        else:
            response = {"error": "نام کاربری یا رمز عبور معتبر نیست."}
            return render(request, self.template_name, context=response)


class RegisterView(View):
    template_name = 'auth/register.html'

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('profile')

        return render(request, self.template_name)

    def post(self, request, *args, **kwargs):
        username = request.POST.get('username')
        email = request.POST.get('email')
        fname = request.POST.get('fname')
        lname = request.POST.get('lname')
        password = request.POST.get('password')

        if username == '' or email == '' or fname == '' or lname == '' or password == '':
            response = {"error": "تمامی فیلدها را باید پر کنید."}
            return render(request, self.template_name, context=response)

        pattern = r'^((?!\.)[\w\-_.]*[^.])(@\w+)(\.\w+(\.\w+)?[^.\W])$'
        check = re.search(pattern, email)
        if not check:
            response = {"error": "ایمیل وارد شده معتبر نیست."}
            return render(request, self.template_name, context=response)

        user = User.objects.filter(username=username)
        if user.exists():
            response = {"error": "این نام کاربری قبلا انتخاب شده است."}
            return render(request, self.template_name, context=response)

        user = User.objects.filter(email=email)
        if user.exists():
            response = {"error": "حساب کاربری با این ایمیل وجود دارد."}
            return render(request, self.template_name, context=response)

        user = User.objects.create_user(username=username, email=email, first_name=fname, last_name=lname, password=password)
        login(request, user)

        return redirect('profile')


class LogoutView(LoginRequiredMixin, View):
    login_url = '/user/login/'

    def get(self, request, *args, **kwargs):
        logout(request)

        return redirect('login')


class ProfileView(LoginRequiredMixin, View):
    template_name = 'profile.html'
    login_url = '/user/login/'

    def get(self, request, *args, **kwargs):
        orders = Order.objects.filter(user=request.user)
        data = {"orders": orders}
        return render(request, self.template_name, context=data)


