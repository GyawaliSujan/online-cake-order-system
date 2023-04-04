from __future__ import unicode_literals

from django.db import models

# Create your models here.


class Contact(models.Model):
    name = models.CharField(max_length=50)
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    message = models.TextField()

    def __unicode__(self):
        return '{}: {}'.format(self.name, self.email)
