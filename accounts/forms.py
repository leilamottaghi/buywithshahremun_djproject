from django import forms
from .models import User ,OtpCode
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password




class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""
    password1 = forms.CharField(label='پسورد', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Password confirmation', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ('email', 'phone_number','full_name')


    # def clean_password1(self):
    #     password1 = self.cleaned_data.get('password1')
    #     try:
    #         password_validation.validate_password(password1, self.instance)
    #     except forms.ValidationError as error:

    #         # Method inherited from BaseForm
    #         self.add_error('password1', error)
    #     return password1

    def clean_password2(self):
        # Check that the two password entries match
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise ValidationError("Passwords don't match")
        return cd['password2']



    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user



class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """
    password = ReadOnlyPasswordHashField(label='پسورد',help_text="you can change password using <a href=\"../password/\">this form</a>")

    class Meta:
        model = User
        fields = ('email', 'phone_number','full_name', 'password','last_login')




class UserRegistrationForm(forms.Form):
    email = forms.EmailField(label='ایمیل')
    full_name = forms.CharField(label='نام و نام خانوادگی')
    phone = forms.CharField(max_length=11,label='شماره موبایل')
    password = forms.CharField(label='پسورد',widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار پسورد',
                                widget=forms.PasswordInput)


    def clean_password(self):
        password = self.cleaned_data['password']
        try:
            validate_password(password)
        except ValidationError as error:
            self.add_error("password", error)
        return password
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] != cd['password2']:
            raise ValidationError('Passwords don\'t match.')
        return cd['password2']

    
    def clean_email(self):
        email = self.cleaned_data['email']
        user = User.objects.filter(email=email).exists()
        if user:
            raise ValidationError('this email already exists')
        else:
            try:
                validation_email = validate_email(email)
            except ValidationError as e:
                print("bad email, details:", e)
            else:
                print("good email")
                return email


    def clean_phone(self):
        phone = self.cleaned_data['phone']
        user = User.objects.filter(phone_number=phone).exists()
        if user:
            raise ValidationError('this phone number already exists')
        OtpCode.objects.filter(phone_number=phone).delete()
        return phone



class VerifyCodeForm(forms.Form):
    code = forms.IntegerField(label='کد')


class UserLoginForm(forms.Form):
	phone = forms.CharField(label='شماره موبایل')
	password = forms.CharField(widget=forms.PasswordInput,label='پسورد')


class PhoneResetPasswordForm(forms.Form):
    phone = forms.CharField(label='شماره موبایل')


class VerifyCodeResetpasswordForm(forms.Form):
    code = forms.IntegerField(label='کد')


class NewPasswordForm(forms.Form):
    newpassword = forms.CharField(widget=forms.PasswordInput, label="پسورد جدید")
    confirm_newpassword = forms.CharField(widget=forms.PasswordInput, label="تکرار پسورد جدید")

    def clean_password(self):
        password = self.cleaned_data['password']
        validate_password(password)
        return password

    def clean_confirm_newpassword(self):
        newpassword = self.cleaned_data['newpassword']
        confirm_newpassword = self.cleaned_data['confirm_newpassword']
        if confirm_newpassword !=newpassword :
            raise ValidationError('confirm_newpassword  is not the same as newpassword ')
        return confirm_newpassword




class UpdatePasswordForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('password',)
        labels = {
            'password': ' پسورد فعلی',
        }
        

    password1 = forms.CharField(label='پسورد جدید', widget=forms.PasswordInput)
    password2 = forms.CharField(label='تکرار پسورد جدید', widget=forms.PasswordInput)

    def clean_password1(self):
        password1 = self.cleaned_data['password1']
        try:
            validate_password(password1)
        except ValidationError as error:
            self.add_error("password1", error)
        return password1
    
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] != cd['password2']:
            raise ValidationError('Passwords don\'t match.')
        return cd['password2']



