from django.contrib import messages
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.decorators import login_required
from django.shortcuts import render

# Create your views here.
from django.utils.crypto import get_random_string

from product.models import Category,Product

from order.models import ShopCart, ShopCartForm, OrderForm, Order, OrderProduct
from user.models import ProfilePro, UserProfile


def index(request):
    return HttpResponse('Order page')

@login_required(login_url='/login')
def addtoshopcart(request,id):
    url = request.META.get('HTTP_REFERER')  # get last url
    current_user = request.user  # Access User Session information
    checkproduct = ShopCart.objects.filter(product_id=id) # Check product in shopcart
    if checkproduct:
        control = 1 # The product is in the cart
    else:
        control = 0 # The product is not in the cart"""

    if request.method == 'POST':  # if there is a post
        form = ShopCartForm(request.POST)
        if form.is_valid():
            if control==1: # Update  shopcart
               data = ShopCart.objects.get(product_id=id)
               data.quantity = form.cleaned_data['quantity']   # qte sera remplacer la qte precedente
               data.save()  # save data
            else : # Insert to Shopcart
                data = ShopCart()
                data.user_id = current_user.id
                data.product_id =id
                data.quantity = form.cleaned_data['quantity']
                data.save()
        messages.success(request, "Product added to Shopcart via F ")
        return HttpResponseRedirect(url)

    else: # if there is no post
        if control == 1:  # Update  shopcart
            data = ShopCart.objects.get(product_id=id)
            #data.quantity += 1  #qte 1 sera ajoutée
            data.quantity = 1  #qte 1 sera remplacée la qté precedente
            data.save()  #
        else:  #  Inser to Shopcart
            data = ShopCart()  # model ile bağlantı kur
            data.user_id = current_user.id
            data.product_id = id
            data.quantity = 1
            data.save()  #
        messages.success(request, "Product added to Shopcart")
        return HttpResponseRedirect(url)

def shopcart(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    total=0
    for rs in shopcart:
        if rs.product.variant == 'None':
            total += rs.quantity * (rs.product.price-(rs.product.price*(rs.product.remise/100)))
        else:
            total += rs.variant.price * rs.quantity



    context = {'shopcart': shopcart,
               'category':category,
               'total' : total
               }
    return render(request, 'shopcart_products.html', context)

@login_required(login_url='/login')
def deletefromcart(request,id):
    ShopCart.objects.filter(id=id).delete()
    messages.success(request, "Your item deleted from Shopcart.")
    return HttpResponseRedirect("/shopcart")


def orderproduct(request):
    category = Category.objects.all()
    current_user = request.user
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    profilepro = ProfilePro.objects.get(user_id=current_user.id)
    total = 0
    for rs in shopcart:
            total += rs.quantity * (rs.product.price-(rs.product.price*(rs.product.remise/100)))

    if request.method == 'POST':
        form = OrderForm(request.POST)
        if form.is_valid():

            # Send Credit card information to bank and get result
            # If payment accepted continue else send payment error to checkout page

            data=Order()
            data.note = form.cleaned_data['note']
            data.user_id = current_user.id
            data.total = total
            data.ip = request.META.get('REMOTE_ADDR')
            ordercode = get_random_string(5).upper()
            data.code = ordercode
            data.save()

            # Save Shopcart items to Order detail items
            shopcart = ShopCart.objects.filter(user_id=current_user.id)
            for rs in shopcart:
                detail = OrderProduct()
                detail.order_id     = data.id # Order Id
                detail.compte = profilepro.compte  # Order Id
                detail.product_id   = rs.product_id
                detail.user_id      = current_user.id
                detail.quantity     = rs.quantity
                detail.price        = rs.product.price
                detail.remise = rs.product.remise
                detail.amount = rs.amount
                detail.order_amount = data.total
                detail.note = data.note
                detail.save()
                #  Reduce product Amount  (quantity)

                product = Product.objects.get(id=rs.product_id)
                product.amount -= rs.quantity
                product.save()

            ShopCart.objects.filter(user_id=current_user.id).delete() # Clear & Delete shopcart
            request.session['cart_items']=0
            messages.success(request, "Your order has been completed. Thank You ")
            return render(request, 'Order_Completed.html',{'ordercode':ordercode, 'category':category})
        else:
            messages.warning(request, form.errors)
            return HttpResponseRedirect("/order/orderproduct")

    form = OrderForm()
    shopcart = ShopCart.objects.filter(user_id=current_user.id)
    profile = UserProfile.objects.get(user_id=current_user.id)
    context = {'shopcart': shopcart,
               'category': category,
               'total': total,
               'profilepro': profilepro,
               'form': form,
               'profile': profile

               }
    return render(request, 'Order_Form.html', context)
