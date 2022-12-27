from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator
from django.db import models

# Create your models here.
from django.forms import ModelForm, TextInput
from product.models import Product


class ShopCart(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField()

    def __str__(self):
        return self.product.title

    def price(self):
        return (self.product.price)

    @property
    def amount(self):
        return (self.quantity * (self.product.price-(self.product.price * (self.product.remise/100))))


class ShopCartForm(ModelForm):
    class Meta:
        model = ShopCart
        fields = ['quantity']
        widgets = {
            'quantity' : TextInput(attrs={'class': 'input','type':'number','value':'1'}),
        }

class Order(models.Model):
    STATUS = (
        ('New','New'),
        ('Export','Export'),

    )
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    code = models.CharField(max_length=5, editable=False)
    note = models.CharField(null=True, max_length=100)
    total=models.FloatField(default=1)
    status = models.CharField(choices=STATUS, default='New', max_length=10)
    ip = models.CharField(blank=True, max_length=20)
    adminnote = models.CharField(null=True, max_length=100)
    date = models.DateField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.first_name

class OrderForm(ModelForm):
    class Meta:
        model = Order
        fields = ['note']

class OrderProduct(models.Model):
    STATUS = (
        ('New', 'New'),
        ('Accepted', 'Accepted'),
        ('Canceled', 'Canceled'),
    )
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    compte = models.CharField(max_length=6, blank=True, null=True)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price=models.FloatField()
    remise = models.FloatField(default=0, validators=[MinValueValidator(0), MaxValueValidator(100)])
    amount = models.FloatField()
    order_amount = models.FloatField()
    note = models.CharField(null=True, max_length=100)
    status = models.CharField(choices=STATUS, default='New', max_length=10)
    date = models.DateField(auto_now_add=True)
    create_at = models.DateTimeField(auto_now_add=True)
    update_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.product.title
