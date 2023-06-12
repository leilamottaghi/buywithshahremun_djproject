from django.contrib import admin
from .models import *
from .models import Order,OrderItem,TestModel
# Register your models here.
# admin.site.register(ShippingAddress)
from admin_comments.admin import CommentInline


admin.site.register(Product)
admin.site.register(Address)


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    raw_id_fields = ('product',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    # list_display  =  ('id','user','updated','paid')
    # list_filter = ('paid','created')
    # ordering = ('paid',)
    list_display  =  ('id','user','updated','status')
    list_filter = ('status','created')
    ordering = ('status',)
    inlines = (OrderItemInline,CommentInline)
    # list_editable = ('status', )


admin.register(TestModel)