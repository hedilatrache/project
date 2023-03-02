from django.shortcuts import render ,redirect
from django.http import JsonResponse
import json
import datetime
from .models import * 
from .utils import cookieCart, cartData, guestOrder
from django.core.paginator import Paginator

from django.contrib.auth.forms import UserCreationForm
from .forms import *
from django.contrib.auth import authenticate , login , logout

from django.contrib import messages

def store(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	products = Product.objects.all().order_by('?')
	
	#pagination

	p= Paginator(Product.objects.all().order_by('?'),6)
	page = request.GET.get('page')
	productlist = p.get_page(page)



	context = {'products':products,'productlist':productlist, 'cartItems':cartItems}
	return render(request, 'store/store.html', context)


def cart(request):
	data = cartData(request)

	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/cart.html', context)

def checkout(request):
	data = cartData(request)
	
	cartItems = data['cartItems']
	order = data['order']
	items = data['items']

	context = {'items':items, 'order':order, 'cartItems':cartItems}
	return render(request, 'store/checkout.html', context)

def updateItem(request):
	data = json.loads(request.body)
	productId = data['productId']
	action = data['action']
	print('Action:', action)
	print('Product:', productId)

	customer = request.user.customer
	product = Product.objects.get(id=productId)
	order, created = Order.objects.get_or_create(customer=customer, complete=False)

	orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

	if action == 'add':
		orderItem.quantity = (orderItem.quantity + 1)
	elif action == 'remove':
		orderItem.quantity = (orderItem.quantity - 1)

	orderItem.save()

	if orderItem.quantity <= 0:
		orderItem.delete()

	return JsonResponse('Item was added', safe=False)

def processOrder(request):
	transaction_id = datetime.datetime.now().timestamp()
	data = json.loads(request.body)

	if request.user.is_authenticated:
		customer = request.user.customer
		order, created = Order.objects.get_or_create(customer=customer, complete=False)
	else:
		customer, order = guestOrder(request, data)

	total = float(data['form']['total'])
	order.transaction_id = transaction_id

	if total == order.get_cart_total:
		order.complete = True
	order.save()

	if order.shipping == True:
		ShippingAddress.objects.create(
		customer=customer,
		order=order,
		address=data['shipping']['address'],
		city=data['shipping']['city'],
		state=data['shipping']['state'],
		zipcode=data['shipping']['zipcode'],
		)

	return JsonResponse('Payment submitted..', safe=False)

# search 
def search(request):
	q=request.GET['q']
	data=Product.objects.filter(name__icontains=q).order_by('-id')
	shop = cartData(request)
	cartItems = shop['cartItems']
	return render(request,'store/search.html',{'data':data,'cartItems':cartItems})

#product detail
def product_detail(request,id):
    product = Product.objects.get(id=id)
    context = {'data':product}
    return render(request,'store/product_detail.html',context)
	
#register

def register(request):
    form = Creationcompte
    if request.method == 'POST':
        regForm = Creationcompte(request.POST)
        if regForm.is_valid():
            user = regForm.save()
            customer = Customer.objects.create(user=user)
            customer.save()
            messages.success(request,'Compte créé avec succès')
        else:
            messages.success(request,'erreur de création du compte')
    return render(request,'registration/register.html',{'form':form})



