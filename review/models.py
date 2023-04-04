from __future__ import unicode_literals

from django.db import models

# Create your models here.


def get_review_image_path(instance, filename):
    return os.path.join('review', str(instance.id), str(instance.id), filename)


class Review(models.Model):
    RATING_CHOICES = (
        (5, '5'),
        (4, '4'),
        (3, '3'),
        (2, '2'),
        (1, '1'),
    )
    name = models.CharField(max_length=50)
    rating = models.PositiveIntegerField(choices=RATING_CHOICES)
    photo = models.ImageField(
        upload_to=get_review_image_path, null=True, blank=True)
    review = models.TextField()

    def __unicode__(self):
        return '{}: {}'.format(self.name, self.rating)
