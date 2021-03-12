from rest_framework import serializers, viewsets
from CoffeeShopTask import models
from django.contrib.auth.models import User

from CoffeeShopTask.models import Order, Product, CustomizationOptions


class CustomizationOptionsSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.CustomizationOptions
        fields = ['option_name']


class CustomizationSerializer(serializers.ModelSerializer):
    options = CustomizationOptionsSerializer(many=True)

    class Meta:
        model = models.Customization
        fields = ['name', 'options']


class ProductSerializer(serializers.ModelSerializer):
    customizations = CustomizationSerializer(many=True, allow_null=True)

    class Meta:
        model = models.Product
        fields = ['name', 'price', 'customizations']


class ProductInOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Product
        fields = ['name', 'price']


class UserSerializer(serializers.ModelSerializer):
    orders = "OrderSerializer"

    class Meta:
        model = User
        fields = ['id', 'username', 'orders']


class OwnerSerializer(serializers.ModelSerializer):
    orders = "OrderSerializer"

    class Meta:
        model = User
        fields = ['id', 'username']


class OrderListSerializer(serializers.ModelSerializer):
    products = ProductInOrderSerializer(read_only=True, many=True)
    customization_options = CustomizationOptionsSerializer(read_only=True, many=True)

    class Meta:
        model = models.Order
        fields = ['id', 'created_time', 'owner', 'status', 'products', 'customization_options']
        read_only_fields = ['status']


class OrderUpdateSerializer(serializers.ModelSerializer):
    products = ProductInOrderSerializer(read_only=True, many=True)
    customization_options = CustomizationOptionsSerializer(read_only=True, many=True)

    class Meta:
        model = models.Order
        fields = ['id', 'created_time', 'owner', 'status', 'products', 'customization_options']



class OrderSerializer(serializers.ModelSerializer):

    class Meta:
        model = models.Order
        fields = ['id', 'created_time', 'owner', 'status', 'products', 'customization_options']
        read_only_fields = ['status', 'owner']

    def create(self, validated_data):
        products_data = validated_data.pop('products')
        customization_options_data = validated_data.pop('customization_options')
        related_products = []
        related_customization_options = []
        self.validate_product_existence(products_data, related_products)
        self.validate_customization_options_existence(customization_options_data, related_customization_options)
        self.validate_options_for_products(customization_options_data, products_data)
        order = Order.objects.create(**validated_data)
        order.customization_options.set(related_customization_options)
        order.products.set(related_products)
        return order

    def validate_options_for_products(self, customization_options_data, products_data):
        if len(products_data) != len(customization_options_data):
            raise Exception("invalid order!")
        for i in range(len(products_data)):
            contains_flag = False
            for customization in products_data[i].customizations.all():
                if customization.options.filter(
                        option_name=customization_options_data[i].__str__().split()[1]).exists():
                    contains_flag = True
                    break
            if not contains_flag:
                raise Exception("invalid customization option for product: " + products_data[i].__str__())

    def validate_customization_options_existence(self, customization_options_data, related_customization_options):
        for customization_options in customization_options_data:
            try:
                related_customization_option = CustomizationOptions.objects.get(
                    option_name=customization_options.__str__().split()[1])
                related_customization_options.append(related_customization_option)
            except Exception as ex:
                # print(ex)
                raise ex

    def validate_product_existence(self, products_data, related_products):
        for product in products_data:
            try:
                product_object = Product.objects.get(name=product)
                related_products.append(product_object)
            except:
                raise Exception("product: not found")

