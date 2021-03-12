from django.db import models


class Product(models.Model):
    name = models.CharField(max_length=50)
    price = models.PositiveIntegerField()

    def __str__(self):
        return self.name


class Customization(models.Model):
    name = models.CharField(max_length=50)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, related_name="customizations",
                                related_query_name="customizations", null=True)

    def __str__(self):
        return self.name


class CustomizationOptions(models.Model):
    option_name = models.CharField(max_length=50)
    customization = models.ForeignKey(Customization, on_delete=models.CASCADE, related_name="options",
                                      related_query_name="options")

    def __str__(self):
        return self.customization.__str__() + " " + self.option_name


class Order(models.Model):
    class Status(models.TextChoices):
        WAITING = ' waiting', 'Waiting'
        PREPARATION = 'preparation', 'Preparation'
        READY = 'ready', 'Ready'
        DELIVERED = 'delivered', 'Delivered'

    created_time = models.DateTimeField(auto_now_add=True)
    owner = models.ForeignKey('auth.User', related_name='orders', on_delete=models.CASCADE)
    status = models.CharField(max_length=11, choices=Status.choices, default=Status.WAITING)
    products = models.ManyToManyField(to=Product, related_name='orders')
    customization_options = models.ManyToManyField(to=CustomizationOptions, related_name='orders')

    def __str__(self):
        return self.created_time.__str__() + "_" + self.owner.username + "_" + self.status

    class Meta:
        ordering = ['created_time']

