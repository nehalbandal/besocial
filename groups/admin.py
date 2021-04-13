from django.contrib import admin
from .models import Group, GroupMember
# Register your models here.

class GroupMemberInline(admin.TabularInline):
    model = GroupMember

from users.admin import admin_site
admin_site.register(Group)