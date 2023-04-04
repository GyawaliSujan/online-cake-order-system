from django.contrib.sitemaps import Sitemap
from django.core.urlresolvers import reverse
from product.models import Cake


class StaticSitemap(Sitemap):

    def items(self):
        return [
            'home',
            'about',
            'faq',
            'privacy_policy',
            'terms_and_condition',
            'contact'
        ]

    def location(self, item):
        return reverse(item)


class ProductSitemap(Sitemap):

    def items(self):
        return Cake.objects.all()

    def location(self, item):
        return reverse('product_detail', args=[item.id, item.slug])
