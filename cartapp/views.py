from django.shortcuts import render, redirect

from .models import Cart, Cart_Item
from goodapp.models import Good, Picture
from authapp.models import Buyer
from orderapp.models import Order, Order_Item
from authapp.forms import RegistrationForm


class Item(object):
	
	good 	= Good
	image 	= Picture

def create_cart(request):

	cart_id 			= request.session.get("cart_id")

	cart 				= Cart()

	if request.user.is_authenticated:
		cart.user = request.user
	else:
		cart.user = None

	cart.save()
	request.session['cart_id'] = cart.id

	return cart	


def get_cart(request):

	cart_id 		= request.session.get("cart_id")
	
	if request.user.is_authenticated:
		cart 		= Cart.objects.filter(user = request.user).last()
	else:			
		cart 		= Cart.objects.filter(id = cart_id).last()
			
	return cart


def show_cart(request):

	cart 				= get_cart(request)
	cr_summ = 0
	table = []
	if cart is None:
		pass
	else:	
		items 	 = Cart_Item.objects.filter(cart = cart)
		for item in items:

			cr_item = Item()

			cr_item.price = item.price

			cr_item.quantity = item.quantity

			cr_item.summ = item.summ

			cr_summ += item.summ
		
			cr_item.good = item.good
			
			images = Picture.objects.filter(good=item.good, main_image=True).first()

			cr_item.image = images
		 	
			table.append(cr_item)


	context = {'table': table, 'cr_summ': cr_summ}
	
	return render(request, '*', context)


def cart_add_item(request, slug):

	if request.method == 'POST':

		quantity 	= int(request.POST.get('quantity'))

	else:
		quantity 	= 1

	cart 			= get_cart(request)

	if cart == None:

		cart = create_cart(request)

	good 				= Good.objects.get(slug = slug)	
	item 				= Cart_Item.objects.all().filter(cart=cart, good=good).first()
	if item is None:	
		summ 			= quantity * good.price
		item 			= Cart_Item(cart = cart, good = good, quantity = quantity, price = good.price, summ = summ)
		
	else:			
		item.quantity	= item.quantity + quantity
		item.summ		= item.quantity * item.price

	item.save()

	cart_items = Cart_Item.objects.filter(cart=cart)

	current_path = request.META['HTTP_REFERER']
	return redirect(current_path)


def cart_del_item(request, slug):
	cart 	= get_cart(request)
	if not cart is None:	
		good 	= Good.objects.get(slug = slug)
		item 	= Cart_Item.objects.filter(cart = cart, good = good).delete()

	cart_items 	= Cart_Item.objects.filter(cart=cart)

	current_path = request.META['HTTP_REFERER']
	return redirect(current_path)


def cart_checkout(request):

	context = {

	}
	if request.user.is_authenticated:
		buyer = Buyer.objects.filter(user=request.user).first()

		if buyer is not None:
			
			context.update({'buyer': buyer})

	return render(request, 'cartapp/checkout.html', context)


def place_order(request):

	if request.method == 'POST':
		price_form = RegistrationForm(request.POST)
		if price_form.is_valid():

			userfirst_name 	= price_form.cleaned_data['userfirst_name']
			userlast_name 	= price_form.cleaned_data['userlast_name']
			companyname 	= price_form.cleaned_data['companyname']
			useremail 		= price_form.cleaned_data['useremail']
			usertel 		= price_form.cleaned_data['usertel']	

			new_order 				= Order()
			if request.user.is_authenticated:

				buyer = Buyer.objects.filter(user=request.user).first()
				if buyer is not None:
					new_order.buyer = buyer
				else:	
					buyer = Buyer(first_name=userfirst_name, last_name=userlast_name, Phone=usertel, email=useremail)
					buyer.user = request.user
					buyer.save()
					new_order.buyer = buyer
			else:
				buyer = Buyer(first_name=userfirst_name, last_name=userlast_name, Phone=usertel, email=useremail)
				buyer.save()
				new_order.buyer = buyer

			cart = get_cart(request)

			new_order.summ = cart.summ
			new_order.save()

			for cart_item in Cart_Item.objects.all().filter(cart=cart):
				order_item 	= Order_Item(order = new_order, good = cart_item.good, quantity = cart_item.quantity, price = cart_item.price, summ = cart_item.summ)
				order_item.save()

			cart.delete()

			return HttpResponse('{}{}'.format(userfirst_name,userlast_name))


