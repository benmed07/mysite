from django.contrib import admin

# Register your models here.
from import_export.admin import ImportExportModelAdmin
from order.models import ShopCart, OrderProduct, Order




class ShopCartAdmin(admin.ModelAdmin):
    list_display = ['user', 'product','quantity','price','amount']
    list_filter = ['user']

class OrderProductline(admin.TabularInline):
    model = OrderProduct
    list_display = ['product_id', 'quantity', 'price', 'remise', 'amount']
    readonly_fields = ('user','product','price','quantity','remise','amount')
    can_delete = False
    extra = 0



class OrderAdmin(ImportExportModelAdmin):
    list_display = ['id','total','status','note']
    list_filter = ['status']
    readonly_fields = ('user','note','total','ip')
    can_delete = False
    inlines = [OrderProductline]

class OrderProductAdmin(ImportExportModelAdmin):
    list_display = ['order_id','user','compte','product_id','quantity','price','remise','amount','date','order_amount','note']
    list_filter = ['date','order_id', 'compte']
    readonly_fields = ['user']

admin.site.register(ShopCart,ShopCartAdmin)

admin.site.register(Order,OrderAdmin)
admin.site.register(OrderProduct,OrderProductAdmin)
