from django.urls import path,include
from .views import (shop_index,
                    groups_list,
                    products_list,
                    orders_list,
                    create_product,
                    create_order,ShopIndexView,
                    GroupsListView,
                    ProductDetailViews,
                    ProfuctListView,
                    OrderListView,
                    OrderDetailtView,ProductCreateView,
                    ProductUpdateView,ProductDelateView,
                    OrderCreateView,OrderUpdateView,
                    OrdertDelateView,ProductViewSet,OrderViewSet,
                    ProductDataExportView,UserOrdersListView)
from rest_framework.routers import DefaultRouter
from django.views.decorators.cache import cache_page

app_name = "shopapp"
routers = DefaultRouter()
routers.register('products',ProductViewSet)

routers.register('orders',OrderViewSet)


urlpatterns = [
    #path("",cache_page(10 * 2)(ShopIndexView.as_view()),name='index'),
    path("",ShopIndexView.as_view(),name='index'),
    path("export/", ProductDataExportView.as_view(), name="export"),
        
    path("groups/",GroupsListView.as_view(),name='groups_list'),
    path('products/',ProfuctListView.as_view(),name='products_list_url'),
    # path('products/create/',create_product,name='product_create_url'),
    path('products/create/',ProductCreateView.as_view(),name='product_create_url'),
    path('products/<int:pk>',ProductDetailViews.as_view(),name='product_details_url'),
    path('products/<int:pk>/update/',ProductUpdateView.as_view(),name='product_update_url'),
    path('products/<int:pk>/delete/',ProductDelateView.as_view(),name='product_delete_url'),

    path('api/',include(routers.urls)),
    
    path('orders/',OrderListView.as_view(),name='orders_list_url'),
    # path('orders/create/',create_order,name='order_create_url'),
    path('orders/create/',OrderCreateView.as_view(),name='order_create_url'),
    path('orders/<int:pk>/',OrderDetailtView.as_view(),name='order_details_url'),
    path('orders/<int:pk>/update/',OrderUpdateView.as_view(),name='order_update_url'),
    path('orders/<int:pk>/delete/',OrdertDelateView.as_view(),name='order_delete_url'),
    path("users/<int:user_id>/orders/", UserOrdersListView.as_view(), name='users_orders_list'),
]
