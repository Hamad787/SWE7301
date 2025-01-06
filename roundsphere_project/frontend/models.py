from django.db import models

class Product(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        app_label = 'frontend'

    def __str__(self):
        return self.name


class Order(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'frontend'

    def __str__(self):
        return f"Order {self.id} - {self.product.name}"


class MeasurementData(models.Model):
    device_id = models.CharField(max_length=255)
    temperature = models.FloatField()
    humidity = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        app_label = 'frontend'

    def __str__(self):
        return f"Measurement {self.id} - {self.device_id}"


class Payment(models.Model):
    order = models.OneToOneField(Order, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=100)
    timestamp = models.DateTimeField(auto_now_add=True)
    class Meta:
        app_label = 'frontend'

    def __str__(self):
        return f"Payment {self.id} - {self.status}"
