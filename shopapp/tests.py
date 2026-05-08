from string import ascii_letters
from  random import choices

from django.contrib.auth.models import User, Permission
from django.test import TestCase
from django.urls import reverse
from .utils import add_two_numbers
from .models import Product, Order

class AddTwoNumbersTestCase(TestCase):
    def test_add_two_numbers(self):
        result = add_two_numbers(2, 3)
        self.assertEqual(result, 5)

class ProductCreateViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.user = User.objects.create_user(username='admin', password='ks040159')
        permission_product = Permission.objects.get(codename='add_product')
        cls.user.user_permissions.add(permission_product)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.product_name = "".join(choices(ascii_letters, k=10))
        Product.objects.filter(name=self.product_name).delete()

    def test_create_product(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse('shopapp:product_create'),
            {
                'name': self.product_name,
                'price': '123.45',
                'discription': 'A good table',
                'discount': '10',
            }
        )
        self.assertRedirects(response, reverse('shopapp:products_list'))
        self.assertTrue(
            Product.objects.filter(name=self.product_name).exists()
        )

class ProductDetailsViewTestCase(TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.product = Product.objects.create(name='Best Product')

    @classmethod
    def tearDownClass(cls) -> None:
        cls.product.delete()

    def test_get_product(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_get_product_and_chek_content(self):
        response = self.client.get(
            reverse('shopapp:product_details', kwargs={'pk': self.product.pk})
        )
        self.assertContains(response, self.product.name)

class ProductsListViewTestCase(TestCase):

    fixtures = [
        'product_fixture.json',
    ]

    def test_products(self):
        response = self.client.get(reverse('shopapp:products_list'))
        self.assertQuerySetEqual(
            qs=Product.objects.filter(archived=False).all(),
            values=(p.pk for p in response.context['product']),
            transform=lambda p: p.pk,
        )
        self.assertTemplateUsed(response, 'shopapp/products-list.html')

class ProductsExportViewTestCase(TestCase):
    fixtures = [
        'product_fixture.json',
    ]

    def test_get_products_view(self):
        response = self.client.get(
            reverse('shopapp:products-export')
        )
        self.assertEqual(response.status_code, 200)
        products = Product.objects.order_by('pk').all()
        expected_data = [
            {
                'pk': products.pk,
                'name': products.name,
                'price': str(products.price),
                'archived': products.archived,
            }
            for product in products
        ]
        products_data = response.json()
        self.assertEqual(
            products_data['products'],
            expected_data,
        )

class OrderDetailViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username='admin', password='ks040159')
        # permission_order = Permission.objects.get(codename='view_order')
        # cls.user.user_permissions.add(permission_order)

    @classmethod
    def tearDownClass(cls):
        cls.user.delete()

    def setUp(self) -> None:
        self.client.force_login(self.user)
        self.order = Order.objects.create(
            delivery_address='ul pupkina',
            promocode='123',
            user=self.user
        )

    def test_order_details(self):
        response = self.client.get(reverse(
            'shopapp:order_details',
            kwargs={'pk': self.order.pk})
        )
        self.assertContains(response, self.order.delivery_address)
        self.assertContains(response, self.order.promocode)
        self.assertContains(response, self.order.pk)

class OrdersExportViewTestCase(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.user = User.objects.create(username='admin', password='ks040159', is_staff=True)
        # permission_order = Permission.objects.get()
        # cls.user.user_permissions.add(permission_order)
        cls.user.save()
    fixtures = [
        'order_fixture.json',
    ]

    def test_get_orders_view(self):
        self.client.force_login(self.user)
        response = self.client.get(
            reverse('shopapp:orders-export')
        )
        self.assertEqual(response.status_code, 200)
        orders = Order.objects.order_by('pk').all()
        expected_data = [
            {
                'id': orders.id,
                'delivery_address': orders.delivery_address,
                'customer_id': orders.customer.id,
                'promocode': orders.promocode
            }
            for order in orders
        ]
        orders_data = response.json()
        self.assertEqual(
            orders_data['products'],
            expected_data,
        )