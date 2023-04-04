from __future__ import unicode_literals


from django.conf import settings
from django.db import models
from django.utils.translation import ugettext_lazy as _


# Create your models here.
class Profile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, related_name='profile')
    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=14)
    location = models.CharField(max_length=200)
    created_on   = models.DateField(auto_now_add=True)

    def __str__(self):
        return "%s's profile" % self.user

    def __unicode__(self):
        return '{}'.format(self.name)
