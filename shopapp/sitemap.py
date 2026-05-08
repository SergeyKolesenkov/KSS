from django.contrib.sitemaps import Sitemap
from django.urls import reverse

from .models import Product


class ShopSiteMap(Sitemap):
    changefreq = 'never'
    priority = 0.8

    def items(self):
        print(Product.objects.all())
        return Product.objects.all()

    def lastmod(self, obj: Product):
        print(obj.created_at)
        return obj.created_at


