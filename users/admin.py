from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .forms import CustomUserCreationForm, CustomUserChangeForm
from .models import CustomUser
from django.contrib.admin import AdminSite
from .views import UpdateUserProfile

class MyAdminSite(AdminSite):
    def get_urls(self):
        from django.urls import path
        urls = super(MyAdminSite, self).get_urls()
        # Note that custom urls get pushed to the list (not appended)
        # This doesn't work with urls += ...
        print("URLS: ", urls)
        urls = [
            path('my_view/<int:pk>/edit/', self.admin_view(UpdateUserProfile.as_view()))
        ] + urls
        return urls

admin_site = MyAdminSite()


class CustomUserAdmin(UserAdmin):
    add_form = CustomUserCreationForm
    form = CustomUserChangeForm
    model = CustomUser
    list_display = ('email', 'username', 'fullname', 'dob', 'gender', 'is_staff', 'is_active',)
    list_filter = ('email', 'is_staff', 'is_active',)
    fieldsets = (
        (None, {'fields': ('email', 'password')}),
        ('User Information', {'fields': ('username', 'fullname', 'dob', 'gender', 'bio', 'profile_pic')}),
        ('Permissions', {'fields': ('is_staff', 'is_active')}),
    )
    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': ('username', 'fullname', 'email', 'dob', 'gender', 'bio', 'profile_pic', 'password1', 'password2', 'is_staff', 'is_active')}
        ),
    )
    search_fields = ('email',)
    ordering = ('email',)


admin_site.register(CustomUser, CustomUserAdmin)