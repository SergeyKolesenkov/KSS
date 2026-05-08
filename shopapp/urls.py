from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import (ShopIndexView,
                    GroupsListView,
                    ProductListView,
                    OrderListView,
                    ProductCreateView,
                    ProductUpdateView,
                    ProductDetailsView,
                    ProductDeleteView,
                    ProductsDataExportView,
                    OrderDetailView,
                    OrderUpdateView,
                    OrderDeleteView,
                    OrderCreateView,
                    OrdersExportView,
                    ProductViewSet,
                    OrderViewSet,
                    )

app_name = 'shopapp'

routers = DefaultRouter()
routers.register('products', ProductViewSet)
routers.register('orders', OrderViewSet)

urlpatterns = [
    path('', ShopIndexView.as_view(), name='index'),
    path('api/', include(routers.urls)),
    path('groups/', GroupsListView.as_view(), name='groups_list'),
    path('products/export', ProductsDataExportView.as_view(), name='products-export'),
    path('products/', ProductListView.as_view(), name='products_list'),
    path('products/create/', ProductCreateView.as_view(), name='product_create'),
    path('products/<int:pk>/', ProductDetailsView.as_view(), name='product_details'),
    path('products/<int:pk>/update/', ProductUpdateView.as_view(), name="product_update"),
    path('products/<int:pk>/archive/', ProductDeleteView.as_view(), name="product_delete"),
    path('order/', OrderListView.as_view(), name='order_list'),
    path('order/<int:pk>/', OrderDetailView.as_view(), name='order_detail'),
    # path('order/create/', create_order, name='create-order'),
    path('order/create/', OrderCreateView.as_view(), name='order_create'),
    path('order/<int:pk>/update', OrderUpdateView.as_view(), name='order_update'),
    path('order/<int:pk>/delete', OrderDeleteView.as_view(), name='order_delete'),
    path('order/export', OrdersExportView.as_view(), name='orders-export')
]