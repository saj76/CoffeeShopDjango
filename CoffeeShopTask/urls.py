from django.conf.urls import url
from django.urls import path, include
from CoffeeShopTask import views
from rest_framework.routers import DefaultRouter

from CoffeeShopTask.views import OrderList

router = DefaultRouter()
# router.register("product", ProductViewSet, basename="products")
router.register("orders", OrderList, basename="orders")

urlpatterns = [
    path('users/', views.UserList.as_view()),
    path('users/<int:pk>/', views.UserDetail.as_view()),
    path('products/', views.ProductList.as_view()),
    path('products/<int:pk>/', views.ProductDetail.as_view()),
    path('customizations/', views.CustomizationList.as_view()),
    path('customizations/<int:pk>/', views.CustomizationDetail.as_view()),
    # path('orders/', views.OrderList.as_view()),
    # path('orders/<int:pk>/', views.OrderDetail.as_view()),
    path('customization_options/', views.CustomizationOptionsList.as_view()),
    path('customization_options/<int:pk>/', views.CustomizationOptionsDetail.as_view()),
    url('', include(router.urls))
]
