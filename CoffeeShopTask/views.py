import os

from decouple import config
from rest_framework import generics, viewsets, status, permissions
from rest_framework.response import Response

from CoffeeShopTask.email_utils import Util
from CoffeeShopTask.permissions import IsOwnerOrReadOnly
from CoffeeShopTask.serializers import UserSerializer, ProductSerializer, OrderSerializer, \
    CustomizationOptionsSerializer, OrderListSerializer, OrderUpdateSerializer
from CoffeeShopTask.models import Customization, Product, Order, CustomizationOptions
from CoffeeShopTask.serializers import CustomizationSerializer
from django.contrib.auth.models import User


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserDetail(generics.RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class ProductList(generics.ListCreateAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    def get_queryset(self):
        products = Product.objects.all()
        return products


class ProductDetail(generics.RetrieveAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class CustomizationList(generics.ListAPIView):
    queryset = Customization.objects.all()
    serializer_class = CustomizationSerializer


class CustomizationDetail(generics.RetrieveAPIView):
    queryset = Customization.objects.all()
    serializer_class = CustomizationSerializer


class OrderList(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly,
                          IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return OrderListSerializer
        if self.action == 'create':
            return OrderSerializer
        if self.action == 'update' or self.action == 'delete':
            return OrderUpdateSerializer
        return OrderListSerializer  # I dont' kno

    def get_queryset(self):
        user = self.request.user
        return user.orders.all()

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    def perform_update(self, serializer):
        if self.is_unauthorized_to_change_order(serializer):
            raise Exception('you have not access to change this order')

        if self.is_status_changing(serializer):
            self.status_change(serializer)
        else:
            self.not_status_order_update(serializer)

    def perform_destroy(self, instance):
        if not self.get_object().status == ' waiting':
            raise Exception('order is not waiting mode. It\'s too late to cancel it.:(')
        instance.delete()
        return Response(data={"status": "success"})

    def status_change(self, serializer):
        self.check_is_admin()
        serializer.save()
        self.send_email_to_order_owner(serializer)

    def is_status_changing(self, serializer):
        previous_status = self.get_object().status
        new_status = serializer.validated_data['status']
        return not previous_status == new_status

    def not_status_order_update(self, serializer):
        instance = self.get_object()
        if not instance.status == ' waiting':
            raise Exception('order is not waiting mode. It\'s too late to change it.:(')
        print("owner " + self.request.user.__str__())
        serializer.save(owner=self.request.user)

    def is_unauthorized_to_change_order(self, serializer):
        return not (self.request.user == serializer.validated_data['owner'] or self.check_is_admin())

    def check_is_admin(self):
        return permissions.IsAdminUser()

    def send_email_to_order_owner(self, serializer):
        print(config('EMAIL_HOST_PASSWORD'))
        previous_status = self.get_object().status
        new_status = serializer.validated_data['status']
        message_notification = """Dear Customer
        your order status has changed: """ + previous_status.__str__() + " -> " + new_status.__str__()
        user_email = User.objects.get(username=serializer.validated_data['owner'])
        data = {'email_body': message_notification, 'email_subject': "CoffeeShop Order Status Change",
                "customer_email": [user_email.email]}
        Util.send_mail(data)


class OrderDetail(generics.RetrieveAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer


class CustomizationOptionsList(generics.ListCreateAPIView):
    queryset = CustomizationOptions.objects.all()
    serializer_class = CustomizationOptionsSerializer

    def get_queryset(self):
        customization_options = CustomizationOptions.objects.all()
        return customization_options


class CustomizationOptionsDetail(generics.RetrieveAPIView):
    queryset = CustomizationOptions.objects.all()
    serializer_class = CustomizationOptionsSerializer
