from django.contrib import admin

# Register your models here.
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .forms import UserCreationForm,UserChangeForm
from .models import User,OtpCode
from django.contrib.auth.models import Group
# Register your models here.


@admin.register(OtpCode)
class OtpCodeAdmin(admin.ModelAdmin):
    list_display = ('phone_number','code','created')

class UserAdmin(BaseUserAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ('email', 'phone_number', 'is_admin','is_superuser')
    list_filter = ('is_admin',)
    readonly_fields = ('last_login',)
    fieldsets = (
        (None, {'fields': ('email','phone_number', 'full_name','password')}),
   
        ('Permissions', {'fields': ('is_active','is_admin','is_superuser','last_login','groups','user_permissions')}),
    )
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = (
        (None, {
            'fields': ('phone_number','email', 'full_name', 'password1', 'password2')
        }),
    )
    search_fields = ('email','full_name')
    ordering = ('full_name',)
    filter_horizontal = ('groups','user_permissions')

    def get_form(self, request,obj=None,**kwargs):
        form = super().get_form(request,obj,**kwargs)
        is_superuser = request.user.is_superuser
        if not is_superuser:
            form.base_fields['is_superuser'].disabled=True
        return form

 
# admin.site.unregister(Group)
# Now register the new UserAdmin...
admin.site.register(User, UserAdmin)
# ... and, since we're not using Django's built-in permissions,
# unregister the Group model from admin.
