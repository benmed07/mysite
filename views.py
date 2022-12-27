import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render

# Create your views here.
from home.models import Setting, ContactForm, ContactMessage
from product.models import Category, Product, Images, Comment, Variants
from home.forms import SearchForm




def index(request):
    setting = Setting.objects.get(pk=1)
    #category = Category.objects.all()
    product_slider = Product.objects.all().order_by('id')[:4]
    product_latest = Product.objects.all().order_by('-id')[:4]
    product_picked = Product.objects.all().order_by('?')[:4]
    page = 'home'
    context = {'setting': setting,
               'page': page,
               'product_slider': product_slider,
               'product_latest': product_latest,
               'product_picked': product_picked
               #'category': category
                }
    return render(request, 'index.html', context)


def aboutus(request):
    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()

    context = {'setting': setting,
               'category': category
               }
    return render(request, 'about.html', context)


def contactus(request):
    # if this is a POST request we need to process the form data
    if request.method == 'POST':
        # create a form instance and populate it with data from the request:
        form = ContactForm(request.POST)
        # check whether it's valid:
        if form.is_valid():
            contactdata = ContactMessage()
            contactdata.name = form.cleaned_data['name']
            contactdata.email = form.cleaned_data['email']
            contactdata.subject = form.cleaned_data['subject']
            contactdata.message = form.cleaned_data['message']
            contactdata.ip = request.META.get('REMOTE_ADDR')
            contactdata.save()

            messages.success(request, "Your message has been sent. Thank You for your interest ")
            return HttpResponseRedirect('/contact')

    setting = Setting.objects.get(pk=1)
    category = Category.objects.all()
    form = ContactForm
    context = {'setting': setting,
               'form': form,
               'category': category
               }
    return render(request, 'contact.html', context)


def category_products(request,id,slug):
    category = Category.objects.all()
    products = Product.objects.filter(category_id=id)
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {'products': products,
               'category':category,
               'page_obj' : page_obj,
                }
    return render(request, 'category_products.html', context)

def search(request):
        if request.method == 'POST':
            form = SearchForm(request.POST)
            if form.is_valid():
                query = form.cleaned_data['query']
                catid = form.cleaned_data['catid']
                if catid==0:
                    products = Product.objects.filter(title__icontains=query)
                else:
                    products = Product.objects.filter(title__icontains=query,category_id=catid)

                category = Category.objects.all()
                context = {'products': products,
                           'category': category}
                return render(request,'search_products.html',context)

        return HttpResponseRedirect('/')

def search_auto(request):
          if request.is_ajax():
            q = request.GET.get('term', '')
            products = Product.objects.filter(title__icontains=q)
            results = []
            for rs in products:
              product_json = {}
              product_json = rs.title
              results.append(product_json)
            data = json.dumps(results)
          else:
            data = 'fail'
          mimetype = 'application/json'
          return HttpResponse(data, mimetype)


@login_required(login_url='/login')
def product_detail(request,id,slug):
    query = request.GET.get('q')
    category = Category.objects.all()
    products = Product.objects.get(pk=id)
    images = Images.objects.filter(product_id=id)
    comments = Comment.objects.filter(product_id=id, status='True')
    context = {'products': products, 'category':category,
               'comments': comments, 'images':images,
               }
    if products.variant != "None": # product have variants
        if request.method == 'POST': #if we select color
            variant_id = request.POST.get('variantid')
            variant = Variants.objects.get(id=variant_id) #selected product by clicking color radio
            colors = Variants.objects.filter(product_id=id,size_id=variant.size_id)
            sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id=%s GROUP BY size_id', [id])
            query += variant.title + 'Size:' + str(variant.size) + ' Color' + str(variant.color)
        else:
            variants = Variants.objects.filter(product_id=id)
            colors = Variants.objects.filter(product_id=id, size_id=variants[0].size_id)
            sizes = Variants.objects.raw('SELECT * FROM product_variants WHERE product_id=%s GROUP BY size_id', [id])
            variant = Variants.objects.get(id=variants[0].id)
        context.update({'sizes':sizes, 'colors':colors,
                        'variant':variant, 'query':query
                        })
    return render(request, 'product_detail.html', context)

@login_required(login_url='/login')
def famille(request):
    category = Category.objects.all()

    context = {'category':category,
               }
    return render(request, 'famille.html', context)
