from django.contrib import admin
from .models import *
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.utils.translation import gettext_lazy as _

User=get_user_model()
# Register your models here.
class SystemUserInlineAdmin(admin.StackedInline):
    model = StaffUser
    can_delete = True
    verbose_name_plural = 'system users'

class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        (_('Personal info'), {'fields': ('first_name', 'last_name', 'email')}),
        (_('Permissions'), {
        'fields': ('is_active', 'is_staff', 'is_superuser'),
    }),
        (_('Important dates'), {'fields': ('last_login', 'date_joined')}),)
    inlines = [SystemUserInlineAdmin]

admin.site.unregister(User)
admin.site.register(User,UserAdmin)