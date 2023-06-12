from django.shortcuts import render
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .forms import *
from django.views.generic import ListView, DetailView, View
from django.http import HttpResponseRedirect
import string
string.ascii_letters
import random
from django.shortcuts import render,get_object_or_404,redirect
from .cart import Cart
from django.contrib.auth.mixins import LoginRequiredMixin
from utils import send_otp_code
from django.contrib import messages
from django.utils import timezone
from datetime import timedelta
import pytz
from django.contrib.auth import login, logout, authenticate
from iranian_cities.models import Province
from iranian_cities.models import County

# سلری    #################################################################################################
from celery.schedules import crontab
from django.http.response import HttpResponse
from django.shortcuts import render
from .tasks import test_func
from send_mail_app.tasks import send_mail_func
from django_celery_beat.models import PeriodicTask, CrontabSchedule
import json
# import pdb; pdb.set_trace()

#selenium -------------

# from selenium import webdriver
# from selenium.webdriver.chrome.service import Service as ChromeService
# from webdriver_manager.chrome import ChromeDriverManager
# from selenium.webdriver.chrome.options import Options
# # options = Options()
# chrome_options = webdriver.ChromeOptions()
# chrome_options.binary_location='C:\Program Files\Google\Chrome Beta\Application\chrome.exe'
# # chrome_options.binary_location='/usr/bin/google-chrome-beta'
# # options.add_argument('headless')
# chrome_options.add_experimental_option( "prefs", {'profile.default_content_settings.images': 2})
# chrome_options.add_experimental_option("detach", True)
# chrome_options.add_argument('--headless')
# chrome_options.add_argument('--no-sandbox')
# chrome_options.add_argument('--disable-dev-shm-usage')
# from crawl_win_breshka import make_ready_bershka

# --------------------Create your views here.---------------------------------------------------------------------



class OstanhaView(View):
    def get(self , request):     
        ostanha = Province.objects.get(code='4')
        print(ostanha)
        return render(request, 'store/ostanha.html',{'ostanha':ostanha})


def test(request):
    test_func.delay()
    return HttpResponse("Done")

def send_mail_to_all(request):
    send_mail_func.delay()
    return HttpResponse("Sent")

def schedule_mail(request):
    schedule, created = CrontabSchedule.objects.get_or_create(hour = 1, minute = 34)
    task = PeriodicTask.objects.create(crontab=schedule, name="schedule_mail_task_"+"5", task='send_mail_app.tasks.send_mail_func')#, args = json.dumps([[2,3]]))
    return HttpResponse("Done")

   #############################################################################################



class MyAddressView(View):
    def get(self , request):     
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'store/address.html',{'addresses':addresses})



class saveAddressView(View):
    def get(self , request):
        form = AddressForm()
        return render(request, 'store/add_address.html',{'form':form})

    def post(self,request):
        msg=None
        form = AddressForm(request.POST)
        #if form.is_valid():
        saveForm=form.save(commit=False)
        saveForm.user=request.user
        # if 'status' in request.POST:
        Address.objects.update(status=False)
        saveForm.save()
        msg = 'Data has been saved'
        form = AddressForm   
        addresses = Address.objects.filter(user=request.user)
        print("aaaaaaaaaaaaaaaaaaaaaaxdcccccccc")
        return render(request, 'store/address.html',{'addresses':addresses})
        


class UpdateAddressView(View): 
    def get(self , request,id):
        address=Address.objects.get(pk=id)
        form = AddressForm(instance=address)
        return render(request, 'store/update_address.html',{'form':form})

    def post(self,request,id):
        address=Address.objects.get(pk=id)
        msg=None
        form = AddressForm(request.POST,instance=address)
        if form.is_valid():
            saveForm=form.save(commit=False)
            saveForm.user=request.user
            if 'status' in request.POST:
                Address.objects.update(status=False)
            saveForm.save()
            msg = 'Data has been saved'
        form = AddressForm(instance=address)   
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'store/address.html',{'addresses':addresses})

        
class DeleteAdressView(View):
    def get(self , request,id):
        Address.objects.filter(id=id).delete()
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'store/address.html',{'addresses':addresses})

class ActivateAddressHrefView(View):
    def get(self , request,id):
        Address.objects.update(status=False)
        Address.objects.filter(id=id).update(status=True)
        addresses = Address.objects.filter(user=request.user)
        return render(request, 'store/address.html',{'addresses':addresses})


# class ActivateAddressView(View):
#     def get(self , request):  
#         a_id = str(request.GET['id'])
#         Address.objects.update(status=False)
#         Address.objects.filter(id=a_id).update(status=True)
#         return JsonResponse({'bool':True})


class OrdersHistoryView(View):
    def get(self , request):
        orders = Order.objects.filter(user=request.user)
        return render(request, 'store/orders_history.html',{'orders':orders})



class OrderDetailsView(View):
    def get(self , request,id):
        order_details=OrderItem.objects.filter(order_id=id)
        order = get_object_or_404(Order,id=id)
        return render(request, 'store/order_items_history.html',{'order_details':order_details, 'order':order})



class EditProfileView(View):
    def get(self , request):
        form = ProfileForm(instance=request.user)
        return render(request, 'store/edit_profile.html',{'form':form})

    def post(self,request):
        form = ProfileForm(request.POST,instance=request.user)
        msg = None
        if form.is_valid():
            
            # cd = form.cleaned_data
            # if cd['password1'] :
            #     print(cd['password1'],"............")
            #     request.user.set_password(cd['password2'])   
            #     request.user.save() 
            form.save()
            msg = 'Data has been saved'
        # form = ProfileForm(instance=request.user)        
        return render(request, 'store/edit_profile.html',{'form':form,'msg':msg})
        


class DashboardView(View):
    def get(self , request):
        return render(request, 'store/my_dashboard.html')


class HomeView(View):
    def get(self , request):
        form = ProductlinkForm() 
        images = [
        {'url': '/static/images/bershka_logo.png', 'alt': 'Image 1'},
        {'url': '/static/images/bershka_logo.png', 'alt': 'Image 2'},
        {'url': '/static/images/bershka_logo.png', 'alt': 'Image 3'},
        {'url': '/static/images/bershka_logo.png', 'alt': 'Image 4'},
        {'url': '/static/images/bershka_logo.png', 'alt': 'Image 5'},
        {'url': '/static/images/bershka_logo.png', 'alt': 'Image 6'},

    ]
        return render(request, 'store/home.html', {'form': form,'images':images })

    def post(self,request):
        form = ProductlinkForm(request.POST)
        print(form)
        if form.is_valid():
            # input("rrrrrrrrrrrrrrrrrrrrrrrreeeeeeeeeeeeees")
            # print(ProductlinkForm(request.POST))
            product_link = form.cleaned_data['product_link']
            print(product_link)
            # product_link = product_link.replace('/','*')
            brands = ['lcwaikiki','ninewest','trendyol','thenorthface','skechers','flo','koton','bershka','mango']
            # browser = webdriver.Chrome(service=ChromeService(ChromeDriverManager(version='104.0.5112.20').install()), options=options)
            for brand in brands:
                if brand in str(product_link):
                    print("find brand crawler ==>>",brand) 
                    # dispatcher={'make_ready_bershka':make_ready_bershka,'browser':browser}
                    # result = eval('make_ready_'+ str(brand) + '("'+ str(product_link) + '",'+'browser'+')',{'__builtins__':None},dispatcher) 
                    # size = result[0]
                    # price =result[1] 
                    # sale_price = result[2]     

                    # weight = "280g"
                    # title = random.choice(string.ascii_letters)
                    # slug = random.choice(string.ascii_letters)
                    # size_crawled = ["s","l"]
                    # size = '|'.join(str(x) for x in size_crawled)
                    # price = "12000"
                    # discount_price = "11000"
                    # description = "it green"
                    # category = "category"
                    # image_list = ['https://kavenegar.com/images/verification/header.png','data:image/jpeg;base64,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']
                    # product = Product.objects.create(product_link=product_link,weight=weight,title=title,slug=slug,sizes=size,description=description,price=price,discount_price =discount_price,category=category)
                    # for img in image_list:
                    #     name_image = random.choice(string.ascii_letters)
                    #     Image.objects.create(image_url=img,name=name_image,product=product)

                    # return redirect('store:productcrawled_detail',slug=slug)
                else:
                    product = Product.objects.create(product_link=product_link,weight='weight',title='title',slug='slug',sizes='size',description='description',price=23,discount_price =23,category='category')
                    
                    # return redirect(reverse('store:product_form',kwargs={'product_link': str(product_link)}))
                    return redirect('store:product_form',product_link)
                    # return redirect(f"product_form/{product_link}")



class ProductFormView(View):
    def get(self,request,product_link):
        print(product_link)
        form1 = ProductForm(prefix="form1")
        form2 = CartAddForm(prefix="form2")
        product = get_object_or_404(Product,product_link=product_link)
        print(form1,":ProductForm")
        return render(request, 'store/product_form.html',{'product':product,'form1':form1,'form2':form2})

    def post(self,request,product_link):
        title = request.POST.get('form1-title')
        print('title:',title)
        size = request.POST.get('form1-sizes')
        print('size:',size)
        weight = request.POST.get('form1-weight')
        print('weight:',weight)
        description = request.POST.get('form1-description')
        print('description:',description)
        discount_price = request.POST.get('form1-discount_price')
        print('discount_price:',discount_price)
        price = discount_price
        print(price)
        selected_quantity = request.POST.get('form2-quantity')
        print('selected_quantity:',selected_quantity)
        tl_price = 3700
        cost = weight
        discount_price_toman=int(((int(discount_price) + 12 ) * tl_price + cost)/1000) * 1000
        pric_toman = discount_price_toman
        Product.objects.filter(product_link = product_link).update(title=title,sizes = size,weight=weight,description=description,discount_price=discount_price_toman,price=pric_toman)
        product = get_object_or_404(Product,product_link=product_link)
        print(product)
        return redirect('store:cart_add',product.id )


        
class ProductDetailView(View):
    form_class = SelectsizeForm
    def get(self,request,slug):
        # product_crawl_session = request.session['pruduct_crawl__info']
        # title = product_crawl_session['title']
        # slug = product_crawl_session['slug']
        # size = product_crawl_session['size']
        # price = product_crawl_session['price']
        # description = product_crawl_session['description']
        # image = product_crawl_session['image']
        product = get_object_or_404(Product,slug=slug)
        title = product.title
        slug = product.slug
        size_str =product.sizes
        size = size_str.split("|")
        list_of_tuples = [(x,x) for x in size]
        form = self.form_class(my_choices=list_of_tuples)
        price = product.price
        discount_price =product.discount_price
        description = product.description
        images = Image.objects.filter(product=product)
        # form_cart_add = CartAddForm()
        form1 = self.form_class(my_choices=list_of_tuples,prefix="form1")
        print(form1,'form1')
        form2 = CartAddForm(prefix="form2")
        print(form2,'form2')
        return render(request, 'store/productcrawled_detail.html',{'product':product,'product_title':title,'product_slug':slug,'product_size':size,'product_price':price,'product_discount_price':discount_price,'product_description':description,'product_image':images,'form1':form1,'form2':form2})

    def post(self,request,slug):
        selected_size = request.POST.get('form1-sizes')
        product_updated = Product.objects.filter(slug = slug).update(sizes = selected_size)
        product = get_object_or_404(Product,slug=slug)
        print("size of product:",product.sizes)
        images = Image.objects.filter(product=product)
        selected_quantity = request.POST.get('form2-quantity')
        print('selected_quantity:',selected_quantity)
        return render(request, 'store/d.html',{'product':product,'images':images})



class CartView(LoginRequiredMixin,View):
    def get(self, request):
        cart = Cart(request)
        print('cart888',cart)
        if cart:
            return render(request , 'store/cart.html',{'cart':cart})
        else:
            return redirect('store:home' )



class CartAddView(View):
    def post(self, request,product_id):
        size = request.POST.get('form1-sizes')
        print('size:',size)
        weight = request.POST.get('form1-weight')
        print('weight:',weight)
        description = request.POST.get('form1-description')
        print('description:',description)
        discount_price = request.POST.get('form1-discount_price')
        print('discount_price:',discount_price)
        price = discount_price
        print(price)
        tl_price = 3700
        cost = float(weight)
        discount_price_toman=float(((float(discount_price) + 12 ) * tl_price + cost)/1000) * 1000
        pric_toman = discount_price_toman
        Product.objects.filter(id = product_id).update(sizes = size,weight=weight,description=description,discount_price=discount_price_toman,price=pric_toman)
        product = get_object_or_404(Product,id=product_id)
        print(product)
        cart = Cart(request)
        product = get_object_or_404(Product,id = product_id)
        # form = CartAddForm(request.POST)
        # if form.is_valid():
        #     cart.add(product, form.cleaned_data['quantity'])
        #     print(cart)
        selected_quantity = request.POST.get('form2-quantity')
        cart.add(product, int(selected_quantity))
        print('cart------>>',cart)
        return redirect('store:cart')




class CartRemoveView(LoginRequiredMixin,View):
    def get(self,request,product_id):
        cart = Cart(request)
        product = get_object_or_404(Product,id = product_id)
        cart.remove(product)
        return redirect('store:cart')



class MinusQuantityCartItemView(LoginRequiredMixin,View):
    def get(self,request,product_id):
        cart = Cart(request)
        product = get_object_or_404(Product,id = product_id)
        cart.minus_quantity_item(product)
        return redirect('store:cart')



class PlusQuantityCartItemView(LoginRequiredMixin,View):
    def get(self,request,product_id):
        cart = Cart(request)
        product = get_object_or_404(Product,id = product_id)
        cart.plus_quantity_item(product)
        return redirect('store:cart')






class NewAddressCheckoutView(LoginRequiredMixin,View):
    def get(self , request,order_id):
        form = AddressForm()
        return render(request, 'store/new_address_checkout.html',{'form':form})

    def post(self,request,order_id):
        msg=None
        form = AddressForm(request.POST)
        if form.is_valid():
            saveForm=form.save(commit=False)
            saveForm.user=request.user
            # if 'status' in request.POST:
                # Address.objects.update(status=False)
            Address.objects.filter(user=request.user).update(status=False)
            saveForm.save()
            msg = 'Data has been saved'
        form = AddressForm   
        addresses = Address.objects.filter(user=request.user)
        return redirect('store:order_detail',order_id)
        

    

class OrderDetailView(LoginRequiredMixin,View):
    # form_comment = CommentCreateForm()
    # form_reply_comment =CommentReplyForm()
    def setup(self, request, *args, **kwargs):
        self.order_instance = get_object_or_404(Order, pk=kwargs['order_id'])
        return super().setup(request, *args, **kwargs)
    
    def get(self, request, order_id):
        # comments = self.order_instance.ocomments.filter(is_reply=False)
        # print("form_comment",self.form_comment)   
        order = get_object_or_404(Order,id=order_id) 
        try:
            address_default = Address.objects.get(user=request.user,status=True)
            print("hgfddddddddddd",address_default)
            form = AddressForm(instance=address_default)
            print(request.user)
            addresses = Address.objects.filter(user=request.user)
            print('addresses--->',addresses)
            # AddressChoices_form= AddressChoicesForm(initial={'Addressoption': 'ALASKA'})
            AddressChoices_Form = AddressChoicesForm(initial={'Addressoption': address_default},prefix='AddressChoices_Form')
            AddressChoices_Form.fields['Addressoption'].queryset = Address.objects.filter(user=request.user)
            print("AddressChoices_Form-initial,",AddressChoices_Form)
            order_details=OrderItem.objects.filter(order_id=order_id)
            # user_name = Address.objects.get(user=request.user,status=1).user_name
            # phone_number = Address.objects.get(user=request.user,status=1).phone_number
            # address = Address.objects.get(user=request.user,status=1).address
            # city = Address.objects.get(user=request.user,status=1).city
            # zip_ = Address.objects.get(user=request.user,status=1).zip
            # status = Address.objects.get(user=request.user,status=1).status
            # form_city = AddressForm(initial={'address':address,'user_name':user_name,'phone_number':phone_number,'city':city,'zip':zip_,'status':status})
            # return render(request,'store/checkout.html',{'form_comment':self.form_comment,'form_reply_comment':self.form_reply_comment,'comments':comments,'addresses':addresses,'order':order,'form':form,'order_details':order_details})
            
            order_comment = OrderComment(prefix='order_comment')
            print('order_comment------->>',order_comment)
            shipping_method_form = ShippingMethodForm(prefix='shipping_method')
            print(shipping_method_form)

            print("shipping_method_formaaaaaaaaaaaaaaaaaa_______",shipping_method_form)


            return render(request,'store/checkout.html',{'shipping_method_form':shipping_method_form,'AddressChoices_Form_initial':AddressChoices_Form,'order_comment':order_comment,'addresses':addresses,'order':order,'form':form,'order_details':order_details})
        except:
            order_details=OrderItem.objects.filter(order_id=order_id)
            order_comment = OrderComment(prefix='order_comment')
            print('order_comment------->>',order_comment)
            form = AddressForm()
            print('formqqqqqqqqqqqqqqqq',form)


            profile_form = AddressForm()
            shipping_method_form = ShippingMethodForm(prefix='shipping_method')
            print("shipping_method_formaaaaaaaaaaaaaaaaaa_______",shipping_method_form)
            return render(request,'store/checkout.html',{'shipping_method_form':shipping_method_form,'profile_form':profile_form,'order_comment':order_comment,'order':order,'form':form,'order_details':order_details})
    
    def post(self, request,order_id): 
        try:
            order_comment = request.POST.get('order_comment-comment')
            print("order_comment:::::::",order_comment)
            # Order.objects.filter(id=order_id).update(comment=order_comment)
            status = True
            address_default = Address.objects.get(user=request.user,status=status)
            # print("address_default +++",address_default)
            # form = AddressForm(request.POST,instance=address_default)
            # print("ggggggggggg",form)
            # if form.is_valid():
            #     print("fffffffffffff")
            cart = Cart(request)
            cart.clear()

            # new_comment = request.POST.get('form_comment-body')
            # if new_comment:
            #     print("new_comment----->>>>",new_comment)
            #     Comment.objects.create(is_reply=0,body=new_comment,order_id=order_id,user_id=request.user.id)
            #     comments = self.order_instance.ocomments.filter(is_reply=False)
            #     return redirect('store:add_comment',order_id)

            AddressChoices_Form = AddressChoicesForm(request.POST,initial={'Addressoption': address_default},prefix='AddressChoices_Form')
            AddressChoices_Form.fields['Addressoption'].queryset = Address.objects.filter(user=request.user)
            print("AddressChoices_Form-initial,",AddressChoices_Form)
            selected_Address = request.POST.get('AddressChoices_Form-Addressoption')
            Order.objects.filter(id=order_id).update(address=selected_Address)
            Address.objects.filter(user=request.user).update(status=False)
            Address.objects.filter(user=request.user).filter(id=selected_Address).update(status=True)
            shipping_method =request.POST.get('shipping_method-shipping_method')
            print(shipping_method)
            Order.objects.filter(id=order_id).update(comment=order_comment,shipping_method=shipping_method)
            # return redirect('store:order_pay',order_id)
            return redirect('store:order_cost_with_shipping_method',order_id)
        
        except:
            form = AddressForm(request.POST)
            if form.is_valid():
                cart = Cart(request)
                cart.clear()
                address_title = request.POST.get('address_title')
                address = request.POST.get('address')
                phone_number = request.POST.get('phone_number')
                zip_code = request.POST.get('zip')
                name = request.POST.get('name')
                last_name = request.POST.get('last_name')
                province = request.POST.get('province')
                county = request.POST.get('county')
                status = request.POST.get('status')
                is_shipping_address = request.POST.get('is_shipping_address')
                status = True
                is_shipping_address = True
                address_new=Address.objects.create(address_title=address_title,county_id=county,province_id=province,user=request.user,name=name,last_name=last_name,address=address,phone_number=phone_number,zip=zip_code, status=status,is_shipping_address=is_shipping_address)
                order_comment = request.POST.get('order_comment-comment')
                print("order_comment:::::::",order_comment)
                shipping_method =request.POST.get('shipping_method-shipping_method')
                print('shipping_method::::::::',shipping_method)
                Order.objects.filter(id=order_id).update(comment=order_comment,address=address_new.id,shipping_method_id=shipping_method)                                          
                # return redirect('store:order_cost_with_shipping_method',order_id)
                return redirect('store:order_cost_with_shipping_method',order_id)
                # return redirect('store:order_pay',order_id)
                
    


class OrderCostWthShippingMethodView(View):
    def get(self, request, order_id):
        order = get_object_or_404(Order,id=order_id)
        print("i succed")
        return render(request,'store/order_cost_with_shipping_method.html',{'order':order})
        # return redirect('store:order_details',order_id)


    

def load_counties(request):
    province_id = request.GET.get('province')
    print(province_id) 
    counties = County.objects.filter(province_id=province_id).order_by('name')
    print("qqqqqqwertyuiop[[[piuytrd]]]",counties)
    return render(request, 'store/county_dropdown_list_options.html', {'counties': counties})




# class OrderAddCommentView(LoginRequiredMixin, View):
#     def post(self, request,order_id):
#         form = CommentCreateForm(request.POST)
#         print(form,"|||||||||||||form_ment")
#         if form.is_valid():
#             print("weeer")
#             new_comment = form.save(commit=False)
#             new_comment.user = request.user
#             order_instance = get_object_or_404(Order, pk=order_id)
#             new_comment.order = order_instance
#             new_comment.save()
#             messages.success(request, 'your comment submitted successfully', 'success')
#             return redirect('store:order_detail', order_id)



# class OrderAddReplyView(LoginRequiredMixin, View):
# 	def post(self, request, order_id, comment_id):
# 		order = get_object_or_404(Order, id=order_id)
# 		comment = get_object_or_404(Comment, id=order_id)
# 		form = CommentReplyForm(request.POST)
# 		if form.is_valid():
# 			reply = form.save(commit=False)
# 			reply.user = request.user
# 			reply.order = order
# 			reply.reply = comment
# 			reply.is_reply = True
# 			reply.save()
# 			messages.success(request, 'your reply submitted successfully', 'success')
# 		return redirect('store:order_detail', order.id)





class OrderCreateView(LoginRequiredMixin, View):
    def get(self,request):
        cart = Cart(request)
        print('useeeeeer-------------------',request.user)
        order = Order.objects.create(user=request.user, comment='',address='')
        for item in cart:
            OrderItem.objects.create(order=order, product=item['product'],price=float(item['price']),quantity=item['quantity'])
        # cart.clear()        
        return redirect('store:order_detail',order.id)



MERCHANT = 'XXXXXXXX-XXXX-XXXX-XXXX-XXXXXXXXXXXX'
ZP_API_REQUEST = "https://api.zarinpal.com/pg/v4/payment/request.json"
ZP_API_VERIFY = "https://api.zarinpal.com/pg/v4/payment/verify.json"
ZP_API_STARTPAY = "https://www.zarinpal.com/pg/StartPay/{authority}"
description = "توضیحات مربوط به تراکنش را در این قسمت وارد کنید" 
CallbackURL = 'http://127.0.0.1:8000/verify/'
# CallbackURL = 'http://localhost:8000/verify/'
# 127.0.0.1  باید بکنیم چون در سشن ها فرق میکنه 


# class OrderPayView(LoginRequiredMixin, View):
class OrderPayView(View):
    def get(self, request, order_id):
        order = Order.objects.get(id=order_id)
        request.session['order_pay'] = {
            'order_id':order_id,
        }
        req_data = {
        "merchant_id": MERCHANT,
        "amount": order.get_total_price(),
        "callback_url": CallbackURL,
        "description": description,
        "metadata": {"mobile": request.user.phone_number, "email":request.user.email}
        }
        req_header = {"accept": "application/json",
                    "content-type": "application/json'"}
        req = requests.post(url=ZP_API_REQUEST, data=json.dumps(
            req_data), headers=req_header)
        authority = req.json()['data']['authority']
        if len(req.json()['errors']) == 0:
            return redirect(ZP_API_STARTPAY.format(authority=authority))
        else:
            e_code = req.json()['errors']['code']
            e_message = req.json()['errors']['message']
            #میتونیم ریدایرکت کنیم به یک صفحه ی دیگه و پیغام خطا نشون بدیم 
            return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")



class OrderVerifyView(LoginRequiredMixin,View):
    def get(self,request):
        order_id = request.session['order_pay']['order_id']
        order = Order.objects.get(id=int(order_id))
        t_status = request.GET.get('Status')
        t_authority = request.GET['Authority']
        if request.GET.get('Status') == 'OK':
            req_header = {"accept": "application/json",
                        "content-type": "application/json'"}
            req_data = {
                "merchant_id": MERCHANT,
                "amount": order.get_total_price(),
                "authority": t_authority
            }
            req = requests.post(url=ZP_API_VERIFY, data=json.dumps(req_data), headers=req_header)
            if len(req.json()['errors']) == 0:
                t_status = req.json()['data']['code']
                if t_status == 100:
                    # order.paid = True
                    # order.save()
                    order.mark_paid(save=False)
                    order.save()
                    return HttpResponse('Transaction success.\nRefID: ' + str(
                        req.json()['data']['ref_id']
                        # یک مدلی برای ذخیره ی کد های ه=تایید ایجاد باید کنم
                    ))
                elif t_status == 101:
                    return HttpResponse('Transaction submitted : ' + str(
                        req.json()['data']['message']
                    ))
                else:
                    return HttpResponse('Transaction failed.\nStatus: ' + str(
                        req.json()['data']['message']
                    ))
            else:
                e_code = req.json()['errors']['code']
                e_message = req.json()['errors']['message']
                return HttpResponse(f"Error code: {e_code}, Error Message: {e_message}")
        else:
            return HttpResponse('Transaction failed or canceled by user')
