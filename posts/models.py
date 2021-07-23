from django.db import models

from social_network_api import settings
class Posts(models.Model):
    _mode_choices = [
        ('PB','Public'),
        ('PR', 'Private')
    ]

    content = models.CharField(max_length=500)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=False, null= False, related_name='post_owner')
    mode = models.CharField(max_length=4, choices=_mode_choices, default='PB')
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    likes = models.ManyToManyField(settings.AUTH_USER_MODEL,related_name='post_like', blank=True)

    def __str__(self) -> str:
        return 'Post #'+ str(self.id)
    


