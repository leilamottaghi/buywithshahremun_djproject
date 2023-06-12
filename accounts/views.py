from django.shortcuts import render,redirect
from django.views import View
from .forms import UserRegistrationForm,VerifyCodeForm ,UserLoginForm,PhoneResetPasswordForm,VerifyCodeResetpasswordForm ,NewPasswordForm,UpdatePasswordForm
import random
from utils import send_otp_code
from .models import OtpCode,User
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import pytz
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.mixins import LoginRequiredMixin

from cryptography.fernet import Fernet
from passlib.hash import pbkdf2_sha256
import re   
  
regex = '^[a-z0-9]+[\._]?[a-z0-9]+[@]\w+[.]\w{2,3}$'  
  
       



class PhoneResetPasswordView(View):
    form_class = PhoneResetPasswordForm
    template_name = 'accounts/phone_reset_password.html'
    def get(self,request):
        form = self.form_class
        return render(request, self.template_name,{'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            # if(re.search(regex,form.cleaned_data['phone'])):   
            #     print("Valid Email") 
            #     # return redirect('password_reset_done')  
            # else:
            try:
                user = User.objects.get(phone_number = form.cleaned_data['phone'])
                if user:
                    print("str is phone")
                    random_code = random.randint(10000,99999)
                    send_otp_code(form.cleaned_data['phone'],code=random_code)
                    OtpCode.objects.create(phone_number=form.cleaned_data['phone'],code=random_code)
                    request.session['user_phone_reset_password_info'] = {
                        'phone_number':form.cleaned_data['phone'],
                    }
                    messages.success(request,'ما یک کد برای شما میفرستیم','success')
                    
                    return redirect('accounts:verify_code_reset_password')
            except:
                messages.success(request,'ما یک کد برای شما میفرستیم','success')   
                return redirect('accounts:user_login')

        return render(request, self.template_name,{'form':form})


class VerifyCodeResetpasswordView(View):
    form_class = VerifyCodeResetpasswordForm
    def get(self,request):
        form = self.form_class
        return render(request,'accounts/verify_code_reset_password.html',{'form':form})
    def post(self,request):
        user_phone_reset_password_session = request.session['user_phone_reset_password_info']
        code_instance = OtpCode.objects.get(phone_number=user_phone_reset_password_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            utc=pytz.UTC
            code_instance.created =code_instance.created.replace(tzinfo=utc)
            if code_instance.created + timedelta(minutes=2) > timezone.now():
                if cd['code'] == code_instance.code:
                    return redirect('accounts:create_new_password')
                    code_instance.delete()
                else:
                    messages.error(request,'این کد اشتباه است','danger')
                    return redirect('accounts:verify_code_reset_password') 
            else:
                messages.error(request,'این کد منقضی شده است','danger')
                return redirect('accounts:phone_reset_password') 
                code_instance.delete()
        return redirect('store:home')



class CreateNewpasswordView(View):
    form_class = NewPasswordForm
    def get(self,request):
        form = self.form_class
        return render(request,'accounts/phone_create_newpassword.html',{'form':form})
    
    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user_phone_reset_password_session = request.session['user_phone_reset_password_info']
            try:
                user = User.objects.get(phone_number = user_phone_reset_password_session['phone_number'])
                if user:
                    user.set_password(cd['confirm_newpassword'])           
                    user.save()
                    code_instance = OtpCode.objects.get(phone_number=user_phone_reset_password_session['phone_number'])
                    code_instance.delete()
                    messages.success(request,'شما یک پسورد جدید ایجاد کردید','success')
                    print(request.user)
                    return redirect('accounts:user_login')
            except:
                return redirect('accounts:user_login')
            
        return render(request,'accounts/phone_create_newpassword.html',{'form':form})




class UpdatePasswordView(View):
    def get(self , request):
        form = UpdatePasswordForm()
        return render(request, 'accounts/update_password.html',{'form':form})
    
    def post(self,request):
        form = UpdatePasswordForm(request.POST)
        if form.is_valid():
            form.save()
            cd = form.cleaned_data 
        form = UpdatePasswordForm()
        
        request.user.set_password(cd['password1'])   
        request.user.save()

        return redirect('accounts:user_login')

    


class UserRegisterView(View):
    form_class = UserRegistrationForm
    template_name = 'accounts/register.html'
    def get(self,request):
        form = self.form_class
        return render(request, self.template_name,{'form':form})

    def post(self, request):
        form = self.form_class(request.POST)
        if form.is_valid():
            random_code = random.randint(1000,9999)
            send_otp_code(form.cleaned_data['phone'],code=random_code)
            OtpCode.objects.create(phone_number=form.cleaned_data['phone'],code=random_code)
            request.session['user_registration_info'] = {
                'phone_number':form.cleaned_data['phone'],
                'email':form.cleaned_data['email'],
                'full_name':form.cleaned_data['full_name'],
                'password':form.cleaned_data['password'],
                'password2':form.cleaned_data['password2'],
            }
            messages.success(request,'ما یک کد برای شما میفرستیم','success')
            
            return redirect('accounts:verify_code')
        return render(request, self.template_name,{'form':form})


class UserRegisterVerifyCodeView(View):
    form_class = VerifyCodeForm
    def get(self,request):
        form = self.form_class
        return render(request,'accounts/verify.html',{'form':form})
    def post(self,request):
        user_session = request.session['user_registration_info']
        code_instance = OtpCode.objects.get(phone_number=user_session['phone_number'])
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # expired_time = datetime.now()-timedelta(minutes=2)
            # OtpCode.objects.filter(created__lt=expired_time).delete()
            utc=pytz.UTC
            code_instance.created =code_instance.created.replace(tzinfo=utc)
            if code_instance.created + timedelta(minutes=2) > timezone.now():
                if cd['code'] == code_instance.code:
                    User.objects.create_user(user_session['phone_number'],user_session['email'],user_session['full_name'],user_session['password'])          
                    code_instance.delete()
                    messages.success(request,'شما با موقیت ثبت نام کردید','success')
                    return redirect('store:home')
                else:
                    messages.error(request,'این کد اشتباه است','danger')
                    return redirect('accounts:verify_code') 
            else:
                messages.error(request,'این کد منقضی شده است ','danger')
                return redirect('accounts:user_register') 
                code_instance.delete()
        return redirect('store:home')



class UserLogoutView(LoginRequiredMixin, View):
	def get(self, request):
		logout(request)
		messages.success(request, 'شما با موفقیت وارد شدید', 'success')
		return redirect('store:home')
        




class UserLoginView(View):
    form_class = UserLoginForm
    template_name = 'accounts/login.html'
    def get(self, request):
        form = self.form_class
        return render(request, self.template_name, {'form':form})
    def post(self, request):
        # valuenext= request.POST.get('next')
        form = self.form_class(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            # user = authenticate(request, password=cd['password'])
            # این اصلی است :

            user = authenticate(request, phone_number=cd['phone'], password=cd['password'])

            if user is not None:
                login(request, user)
                messages.success(request, 'شما با موفقیت وارد شدید', 'info')
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('store:home')
                # return render(request, self.template_name, {'form':form, 'valuenext': valuenext})
            messages.error(request, 'شماره موبایل یا پسوردتان اشتباه است', 'warning')
        return render(request, self.template_name, {'form':form})     