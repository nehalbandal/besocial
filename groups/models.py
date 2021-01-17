from django.db import models
from django.utils.text import slugify
from django.urls import reverse
from django.shortcuts import redirect
import misaka
from django.conf import settings

from django import template
register = template.Library()


class Group(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(allow_unicode=True, unique=True)
    description = models.TextField(blank=True, default='')
    description_html = models.TextField(editable=False, default='', blank=True)
    profile_pic = models.ImageField(upload_to='users/profile_pics', blank=True, default="groups/profile_pics/default_group.png")
    members = models.ManyToManyField(settings.AUTH_USER_MODEL, through='GroupMember')

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        self.slug = slugify(self.name)
        self.description_html = misaka.html(self.description)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('groups:single', kwargs={'slug':self.slug})

    class Meta:
        ordering = ['name']


class GroupMember(models.Model):
    """
    This is an intermediate table created to handle Many To Many relationship between user and group.
    """
    group = models.ForeignKey(Group, related_name='memberships', on_delete=models.CASCADE)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='user_groups', on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username
    
    class Meta:
        # unique_together = ('group', 'user')
        constraints = [models.UniqueConstraint(fields=['group', 'user'], name='user_group')]