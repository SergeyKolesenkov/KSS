# from collections.abc import Sequence
from typing import Sequence
from django.contrib.auth.models import User
from django.core.management import BaseCommand
from shopapp.models import Order, Product
from django.db import transaction


class Command(BaseCommand):
    @transaction.atomic
    def handle(self, *args, **options):
        self.stdout.write('Create order with products')
        user = User.objects.get(username='admin')
        product: Sequence[Product] = Product.objects.defer('description', 'price', 'created_at').all()
        product: Sequence[Product] = Product.objects.only('pk').all()
        order, created = Order.objects.get_or_create(
            delivery_address = 'ul Ivanova, d 8',
            promocode = 'Promo2',
            user = user,
        )

        self.stdout.write(f'Created order {order}')
        for product in product:
            order.products.add(product)
        order.save()
        self.stdout.write(f'Created order {order}')