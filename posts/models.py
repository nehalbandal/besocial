from django.db import models
from django.urls import reverse
from groups.models import Group
import misaka
from django.conf import settings


class Post(models.Model):
    title = models.CharField(max_length=255, blank=False, default='')
    message = models.TextField(blank=True)
    message_html = models.TextField(editable=False, default='', blank=True)
    picture = models.ImageField(upload_to='posts/user_uploads', blank=True)
    created_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='posts', on_delete=models.CASCADE)
    group = models.ForeignKey(Group, related_name='posts', null=True, blank=True, on_delete=models.CASCADE)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.message_html = misaka.html(self.message)
        print("======",self.picture)
        super().save(*args, **kwargs)
        
    def get_absolute_url(self):
        return reverse('posts:single', kwargs=({'username':self.user.username, 'pk':self.pk}))
