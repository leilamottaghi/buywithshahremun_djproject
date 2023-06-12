from django.urls import path,re_path
from . import views
import debug_toolbar
from django.contrib.auth import views as auth_views



app_name = 'store'
urlpatterns = [    
    path('order_cost_with_shipping_method/<int:order_id>/',views.OrderCostWthShippingMethodView.as_view(),name = 'order_cost_with_shipping_method'),
    path('ajax/load-counties/', views.load_counties, name='ajax_load_counties'),
    path('ostanha/',views.OstanhaView.as_view(),name = 'ostanha'),
    path('new_address_checkout/<int:order_id>/',views.NewAddressCheckoutView.as_view(),name = 'new_address_checkout'),
    # path('comment/<int:order_id>/', views.OrderAddCommentView.as_view(), name='add_comment'),
    # path('reply/<int:order_id>/<int:comment_id>/', views.OrderAddReplyView.as_view(), name='add_reply'),
    path('test/', views.test, name="test"),
    path('sendmail/', views.send_mail_to_all, name="sendmail"),
    path('schedulemail/', views.schedule_mail, name="schedulemail"),
    path('my_dashboard/',views.DashboardView.as_view(),name = 'my_dashboard'),
    path('edit_profile/',views.EditProfileView.as_view(),name = 'edit_profile'),
    path('my_address/',views.MyAddressView.as_view(),name = 'my_address'),
    path('add_address/',views.saveAddressView.as_view(),name = 'add_address'),
    path('update_address/<int:id>',views.UpdateAddressView.as_view(),name = 'update_address'),
    path('activate_address_href/<int:id>',views.ActivateAddressHrefView.as_view(),name = 'activate_address_href'),
    path('orders_history/',views.OrdersHistoryView.as_view(),name = 'orders_history'),
    path('order_details/<int:id>',views.OrderDetailsView.as_view(),name = 'order_details'),
    path('delete_address/<int:id>',views.DeleteAdressView.as_view(),name = 'delete_address'),
	path('pay/<int:order_id>/',views.OrderPayView.as_view(),name = 'order_pay'),
    path('verify/',views.OrderVerifyView.as_view(),name = 'order_verify'),
	path('create/',views.OrderCreateView.as_view(),name = 'create'),
    path('checkout/<int:order_id>/',views.OrderDetailView.as_view(),name = 'order_detail'),
	path('cart/',views.CartView.as_view(),name = 'cart'),
    path('cart/add/<int:product_id>/',views.CartAddView.as_view(),name = 'cart_add'),
    path('cart/remove/<int:product_id>/',views.CartRemoveView.as_view(),name = 'cart_remove'),
    path('cart/minus_quantity_cart_item/<int:product_id>/',views.MinusQuantityCartItemView.as_view(),name = 'minus_quantity_cart_item'),
    path('cart/plus_quantity_cart_item/<int:product_id>/',views.PlusQuantityCartItemView.as_view(),name = 'plus_quantity_cart_item'),
	path('<slug:slug>/',views.ProductDetailView.as_view(),name = 'productcrawled_detail'),
	path('',views.HomeView.as_view(),name = 'home'),
    path('product_form/<path:product_link>',views.ProductFormView.as_view(),name = 'product_form'),
]
