from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Wishlist, Wishlist_Item
from goodapp.models import Good, Picture


class Item(object):
	
	good 	= Good
	image 	= Picture


def create_wishlist(request):

	wishlist_id 			= request.session.get("wishlist_id")

	wishlist 			= Wishlist()

	if request.user.is_authenticated:
		wishlist.user = request.user
	else:
		wishlist.user = None

	wishlist.save()
	request.session['wishlist_id'] = wishlist.id

	return wishlist


def get_wishlist(request):

	wishlist_id 		= request.session.get("wishlist_id")
	
	if request.user.is_authenticated:
		wishlist 		= Wishlist.objects.filter(user = request.user).last()
	else:			
		wishlist 		= Wishlist.objects.filter(id = wishlist_id).last()
			
	return wishlist	


def show_wishlist(request):

	wishlist = get_wishlist(request)
	table = []
	if wishlist is None:
		pass
	else:	

		items 	 = Wishlist_Item.objects.filter(wishlist = wishlist)
	
		for item in items:

			wl_item = Item()

			wl_item.price = item.price
		
			wl_item.good = item.good
		
			images = Picture.objects.get(good=item.good, main_image=True)
		
			wl_item.image = images
		 	
			table.append(wl_item)

	wl_count = len(table)

	context = {'table': table, 'wl_count': wl_count, }
	
	return render(request, '*', context)	


def wishlist_add_item(request, slug):

	wishlist 			= get_wishlist(request)
	if wishlist is None:
		wishlist 		= create_wishlist(request)			
	
	good 				= Good.objects.get(slug = slug)
	item 				= Wishlist_Item.objects.filter(wishlist = wishlist, good = good).first()	

	if item is None:	
		item 			= Wishlist_Item(wishlist = wishlist, good = good, price = good.price4)
		item.save()
	else:			
		wishlist_del_item(request, slug)

	current_path = request.META['HTTP_REFERER']
	return redirect(current_path)	


def wishlist_del_item(request, slug):
	
	wishlist 	= get_wishlist(request)
	if not wishlist is None:	

		good 	= Good.objects.get(slug = slug)
		item 	= Wishlist_Item.objects.filter(wishlist = wishlist, good = good).delete()

	current_path = request.META['HTTP_REFERER']
	return redirect(current_path)
