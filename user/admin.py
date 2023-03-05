from django.contrib import admin

from .models import CustomUser, UserImage


@admin.register(CustomUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'is_staff')
    list_display_links = ('username', )


@admin.register(UserImage)
class UserImageAdmin(admin.ModelAdmin):
    list_display = ['title', 'image']