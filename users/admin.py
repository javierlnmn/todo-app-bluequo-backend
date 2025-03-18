from django.contrib.auth.models import Group
from rest_framework.authtoken.models import TokenProxy

from django.contrib import admin
from .models import CustomUser

admin.site.unregister(Group)
admin.site.unregister(TokenProxy)

@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name',)
    search_fields = ('username',)