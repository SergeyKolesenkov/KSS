"""
В этом модуле лежат различные наборы представлений.

Разные view интернет-магазина: по товарам, заказам и т.д.
"""
import logging
from timeit import default_timer

from django.contrib.auth.models import Group
from django.shortcuts import render, redirect, reverse
from django.http import (HttpResponse, HttpRequest,
                         HttpResponseRedirect, JsonResponse)
from django.urls import reverse_lazy
from django.views import View
from django.views.generic import (DetailView, CreateView, ListView,
                                  UpdateView, DeleteView)
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter, OrderingFilter
from django_filters.rest_framework import DjangoFilterBackend
from .models import Order, ProductImage
from .forms import ProductForm, GroupForm, Product, OrderForm
from django.contrib.auth.mixins import (PermissionRequiredMixin,
                                        UserPassesTestMixin, LoginRequiredMixin, )
from .serializers import ProductsSerializer, OrdersSerializer

def home(request):
    return render(request, 'home.html')

log = logging.getLogger(__name__)


class ShopIndexView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        products = [
            ('Laptop', 2000),
            ('Desktop', 3000),
            ('Smartphon', 1000)
        ]
        context = {
            'time_running': default_timer(),
            'products': products,
        }
        log.debug('Products for for shop index: %', products)
        log.info('Rendering shop index')
        return render(request, 'shopapp/shop_index.html', context=context)


@extend_schema(description='Product views CRUD')
class ProductViewSet(ModelViewSet):
    """
    Набор представлений для действий над Product.

    Полный CDUD для сущностей товара
    """

    queryset = Product.objects.all()
    serializer_class = ProductsSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter,]
    search_fields = ['name', 'description']
    filterset_fields = [
        'name',
        'description',
        'discount',
        'price',
        'archived',
    ]
    ordering_fields = [
        'name',
        'description',
        'discount',
    ]

    @extend_schema(
        summary="Get one **product** by ID",
        description='Retrieves product, returns 404 if not found',
        responses={
            200: ProductsSerializer,
            404: OpenApiResponse(description='Empty response, product by id not found'),
        }
    )
    def retrieve(self, *args, **kwargs):
        return super().retrieve(*args, **kwargs)


class OrderViewSet(ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrdersSerializer
    filter_backends = [SearchFilter, DjangoFilterBackend, OrderingFilter,]
    search_fields = ['delivery_address']
    filterset_fields = [
        'user',
        'delivery_address',
        'promocode',
        'created_at',
        'products',
    ]
    ordering_fields = [
        'created_at'
    ]


class GroupsListView(View):
    def get(self, request: HttpRequest) -> HttpResponse:
        context = {
            'form': GroupForm(),
            'groups': Group.objects.prefetch_related('permissions').all(),
        }
        return render(request, 'shopapp/groups-list.html', context=context)

    def post(self, request: HttpRequest):
        form = GroupForm(request.POST)
        if form.is_valid():
            form.save()

        return redirect(request.path)


class ProductDetailsView(DetailView):
    template_name = 'shopapp/product_detail.html'
    queryset = Product.objects.prefetch_related('images')
    context_object_name = 'product'


class ProductUpdateView(UpdateView):
    model = Product
    # fields = 'name', 'price', 'description', 'discount'
    template_name_suffix = '_update_form'
    form_class = ProductForm

    def get_success_url(self):
        return reverse(
            'shopapp:product_details',
            kwargs={'pk': self.object.pk},
        )

    def form_valid(self, form):
        response = super().form_valid(form)
        for image in form.files.getlist('images'):
            ProductImage.objects.create(
                product=self.object,
                image=image,
            )

        return response


class ProductListView(ListView):
    template_name = 'shopapp/products-list.html'
    context_object_name = 'product'
    queryset = Product.objects.filter(archived=False)


class ProductCreateView(PermissionRequiredMixin, CreateView):
    permission_required = 'shopapp.add_product'
    model = Product
    fields = 'name', 'price', 'description', 'discount', 'preview'
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        return super().form_valid(form)


# class ProductUpdateView(PermissionRequiredMixin, UpdateView):
#     permission_required = 'change_product'
#     model = Product
#     fields = 'name', 'price', 'description', 'discount', 'preview'
#     template_name_suffix = '_update_form'
#
#     def test_func(self):
#         return self.request.user == self.get_object().created_by
#         or self.request.user.is_superuser
#     def get_success_url(self):
#         return reverse(
#             "shopapp:product_details",
#             kwargs={"pk": self.object.pk},
#         )


class ProductDeleteView(DeleteView):
    model = Product
    success_url = reverse_lazy('shopapp:products_list')

    def form_valid(self, form):
        success_url = self.get_success_url()
        self.object.archived = True
        self.object.save()
        return HttpResponseRedirect(success_url)


class ProductsDataExportView(View):
    def get(self, request: HttpRequest) -> JsonResponse:
        products = Product.objects.order_by('pk').all()
        products_data = [
            {
                # 'pk': product.pk,
                'name': product.name,
                'price': product.price,
                'archived': product.archived,
            }
            for product in products
        ]
        elem = products_data[0]
        name = elem['name']
        print('name:', name)
        return JsonResponse({'products': products_data})


class OrderListView(LoginRequiredMixin, ListView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
        .all()
    )


class OrderDetailView(DetailView):
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )


class OrderUpdateView(UpdateView):
    model = Order
    fields = 'user', 'promocode', 'delivery_address'
    template_name_suffix = '_update_form'

    def get_success_url(self):
        return reverse(
            'shopapp:order_detail',
            kwargs={'pk': self.object.pk},
        )


class OrderCreateView(CreateView):
    template_name = 'shopapp/order_create.html'
    form_class = OrderForm
    queryset = (
        Order.objects
        .select_related("user")
        .prefetch_related("products")
    )
    success_url = reverse_lazy('shopapp:order_list')


class OrderDeleteView(DeleteView):
    model = Order
    success_url = reverse_lazy('shopapp:order_list')


class OrdersExportView(UserPassesTestMixin, View):
    def test_func(self):
        return self.request.user.is_staff

    def get(self, request: HttpRequest) -> JsonResponse:
        orders = Order.objects.all()
        orders_data = [
            {
                'id': orders.id,
                'delivery_address': orders.delivery_address
                if order.delivery_address else '',
                'customer_id': orders.customer.id if orders.customer else '',
                'promocode': orders.promocode if orders.promocode else '',

            }
            for order in orders
        ]
        return JsonResponse({'products': orders_data})
