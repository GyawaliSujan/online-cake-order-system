from django.db import IntegrityError
from django.db.models import Max
from django.utils.text import slugify


class SlugMixin(object):
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.get_slug()
        try:
            super(SlugMixin, self).save(*args, **kwargs)
        except IntegrityError as e:
            self.slug = self.get_slug(suffixed=True)
            super(SlugMixin, self).save(*args, **kwargs)

    def get_slug(self, suffixed=False):
        slug = slugify(self.name)
        if suffixed:
            id = self.id or self.__class__.objects.aggregate(id=Max("id") + 1).get("id")
            slug += "-{}".format(id)
        return slug