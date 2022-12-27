from django import template
from django.urls import reverse

from mysite import settings

from order.models import ShopCart
from product.models import Category


register = template.Library()


@register.simple_tag
def categorylist():
    return Category.objects.all()


@register.simple_tag
def shopcartcount(userid):
    count = ShopCart.objects.filter(user_id=userid).count()
    return count


@register.simple_tag
def totalcart(userid):
    shopcart = ShopCart.objects.filter(user_id=userid)
    total=0
    for rs in shopcart:
        total += rs.quantity * (rs.product.price - (rs.product.price * (rs.product.remise / 100)))
    return total