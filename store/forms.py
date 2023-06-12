from django import forms
from django_countries.fields import CountryField
from django_countries.widgets import CountrySelectWidget
from accounts.models import User
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from .models import Address,Order,Product,TestModel,ShippingMethod
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.contrib.auth.password_validation import validate_password
from iranian_cities.models import County
from django.core.validators import URLValidator
from django.core.exceptions import ValidationError
from django.forms.widgets import PasswordInput




class ProductForm(forms.ModelForm):
    class Meta:
        model = Product
        fields = ('title','discount_price','sizes','weight','description')
        widgets = {
          'description': forms.Textarea(attrs={'rows':4, 'cols':15}),
        }
    labels = {
            'title': 'عنوان',
        }
    attrs = {'dir': 'rtl'}
    label_suffix = ''

    def __init__(self, *args, **kwargs):
        super(ProductForm, self).__init__(*args, **kwargs)
        for field in self.fields:
            self.fields[field].label_suffix = ''
            self.fields[field].widget.attrs.update({'class': 'form-control', 'dir': 'rtl'})


class ProductlinkForm(forms.Form):
    def validate_example_url(value):
        if not value.startswith('https://'):
            raise ValidationError('Invalid URL: %(value)s', params={'value': value})
    product_link = forms.URLField(label='لینک خود را وارد کنید',validators=[URLValidator(), validate_example_url],widget=forms.URLInput(attrs={'class': 'form-control', 'style': 'display: flex; align-items: center; justify-content: center;width: 50%;'}))
   
    

class FooForm(forms.Form):
    def __init__(self, foo_choices, *args, **kwargs):
        super(FooForm, self).__init__(*args, **kwargs)
        self.fields['foo'].choices = foo_choices
    foo = forms.ChoiceField(choices=(), required=True)



class SelectsizeForm(forms.Form):
    def __init__(self, *args, **kwargs):
        choices = kwargs.pop('my_choices')
        super(SelectsizeForm, self).__init__(*args, **kwargs)
        self.fields["sizes"] = forms.ChoiceField(choices=choices)



class CartAddForm(forms.Form):
    quantity = forms.IntegerField(min_value=1,max_value=100,label='تعداد')


PAYMENT_CHOICES = (
    ('S', 'Stripe'),
    ('P', 'PayPal')
)



class OrderComment(forms.ModelForm):
    comment = forms.CharField(required=False, widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 15, 'placeholder': '... یاداشت خود را وارد کنید'}))

    class Meta:
        model = Order
        fields = ('comment',)
        labels = {
            'comment': 'Your Comment',
        }
        widgets = {
            'comment': forms.Textarea(attrs={'class': 'form-control', 'rows': 4, 'cols': 15, 'placeholder': '... یاداشت خود را وارد کنید', 'required': ''}),
        }
    def crispy_order_comment(self):
        return self['comment'].crispy_tag(label='Your Comment')





class AddressChoicesForm(forms.Form):
    Addressoption = forms.ModelChoiceField(queryset=Address.objects.all(), label="انتخاب آدرس")
    def __init__(self, *args, **kwargs):
        userid = kwargs.pop('userid', None)
        super(AddressChoicesForm, self).__init__(*args, **kwargs)

        if userid:
            self.fields['Addressoption'].queryset = Address.objects.filter(user=userid)




class AddressForm(forms.ModelForm):
    status = forms.BooleanField(disabled = 'disabled',initial=True,label='این اطلاعات را برای خرید بعد استفاده کن',widget=forms.CheckboxInput(attrs={}),required=False)
    is_shipping_address = forms.BooleanField(disabled = 'disabled',initial=True,label='آدرس ارسال با ادرس صورت حساب یکی میباشد ',widget=forms.CheckboxInput(attrs={}),required=False)
    class Meta:
        model = Address
        fields = ('name','last_name','address_title','address','phone_number','zip','is_shipping_address','status','province','county')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['county'].queryset = County.objects.none()
        try:
            if 'province' in self.data:
                try:
                    print(self.data.get('province'))
                    province_id = int(self.data.get('province'))
                    print('province_id--------------0000000000000',province_id)
                    self.fields['county'].queryset = County.objects.filter(province_id=province_id).order_by('name')
                except (ValueError, TypeError):
                    pass 
            elif self.instance.pk:
                print("ohhhhhhhhhhhhh")
                self.fields['county'].queryset = self.instance.province.county_set.order_by('name')
        except:
            return None











class CustomPasswordWidget(PasswordInput):
    def render(self, name, value, attrs=None, renderer=None):
        if value:
            value = value.split('\n')[0]
        return super().render(name, value, attrs, renderer)

class ProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ('full_name','email', 'phone_number', 'password')
        readonly_fields = ('email',)
        
    password = forms.CharField(widget=CustomPasswordWidget()  ,   label='پسورد',help_text=" شما می توانید پسوردتان را با استفاده از لینک زیر تغییر دهید <a href=\"/accounts/update_password/\">فرم تغییر پسورد</a> ")
    # password = ReadOnlyPasswordHashField(label='پسورد',help_text="تغییر دهید<a href=\"/accounts/update_password/\">فرم تغییر پسورد</a>شما می توانید پسوردتان را با استفاده از ")
   

    def __init__(self, *args, **kwargs):
        super(ProfileForm, self).__init__(*args, **kwargs)
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            print("yes ins")
            self.fields['phone_number'].widget.attrs['readonly'] = True
            for field in self.fields:
                self.fields[field].label_suffix = ''
                self.fields[field].widget.attrs.update({'class': 'form-control', 'dir': 'rtl'})

 
    def clean_phone_number(self):
        instance = getattr(self, 'instance', None)
        if instance and instance.pk:
            return instance.phone_number
        else:
            return self.cleaned_data['phone_number']





class ShippingMethodForm(forms.Form):
    shipping_method = forms.ModelChoiceField(queryset=ShippingMethod.objects.all(), widget=forms.RadioSelect, label=" نحوه ی ارسال")
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.initial['shipping_method'] = ShippingMethod.objects.first()




# class CommentCreateForm(forms.ModelForm):
# 	class Meta:
# 		model = Comment
# 		fields = ('body',)
# 		widgets = {
# 			'body': forms.Textarea(attrs={'class':'form-control'})
# 		}


# class CommentReplyForm(forms.ModelForm):
# 	class Meta:
# 		model = Comment
# 		fields = ('body',)
        


