from django.contrib import admin
from Accounts.models import CustomUser,Profile

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'email', 'username', 'employee_id', 'is_staff', 'is_active', 'date_joined')
    list_filter = ('is_staff', 'is_active')
    search_fields = ('email', 'username', 'employee_id')
    

@admin.register(Profile)
class profileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'profile_photo','mobile_number','address')
    search_fields = ('user__email',)