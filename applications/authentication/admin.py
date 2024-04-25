from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import CustomUser, UploadedFile, Notification, Contact


class CustomUserAdmin(UserAdmin):
    # Customize the fields displayed in the list view
    list_display = ('email', 'first_name', 'last_name', 'is_staff', 'is_superuser',)
    readonly_fields = ("date_joined",)
    # Customize the fields displayed in the add/edit forms
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'birthdate', 'profile_img', 'card_number', 'solde')}),
        # ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser', 'groups', 'user_permissions')}),
        ('Important dates', {'fields': ('last_login', 'date_joined')}),
    )
    # Customize the add form
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
                'email',
                'password1',
                'password2',
                'first_name',
                'last_name',
                'profile_img',
                'birthdate',
                'card_number',
                'solde',
            ),
        }),
    )
    # Customize the search fields
    search_fields = ('email',)
    # Customize the ordering of records
    ordering = ('email',)

admin.site.register(CustomUser, CustomUserAdmin)
admin.site.register(Notification)
admin.site.register(UploadedFile)
admin.site.register(Contact)
