from django.urls import path,include
from . import views
from django.contrib.auth import views as auth_views


app_name = 'accounts'
urlpatterns = [
    path('register/',views.UserRegisterView.as_view(),name='user_register'),
    path('verify/',views.UserRegisterVerifyCodeView.as_view(),name='verify_code'),
    path('login/', views.UserLoginView.as_view(), name='user_login'),
    path('logout/', views.UserLogoutView.as_view(), name='user_logout'),

    path('phone_reset_password/',views.PhoneResetPasswordView.as_view(),name='phone_reset_password'),
    path('verify_code_reset_password/',views.VerifyCodeResetpasswordView.as_view(),name='verify_code_reset_password'),
    path('create_new_password/',views.CreateNewpasswordView.as_view(),name='create_new_password'),

    path('update_password/',views.UpdatePasswordView.as_view(),name = 'update_password'),

]

# path('reset_password/', auth_views.PasswordResetView.as_view(template_name ="accounts/password_reset.html"), name='reset_password'),
# path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(template_name ="accounts/password_reset_sent.html"), name='password_reset_done'),
# path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(template_name ="accounts/password_reset_confirm.html"), name='password_reset_confirm'),
# path('reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(template_name ="accounts/password_reset_done.html"), name='password_reset_complete'),
