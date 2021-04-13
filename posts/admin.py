from django.contrib import admin
from .models import Post

from users.admin import admin_site

admin_site.register(Post)