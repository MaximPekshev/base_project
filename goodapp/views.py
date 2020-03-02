from django.shortcuts import render
from .models import Good
from .models import Picture
from django.core.paginator import Paginator
from cartapp.views import Cart_View
from wishlistapp.views import Wishlist_View
from wishlistapp.models import Wishlist_Item


class Item(object):
	
	good 	= Good
	image 	= Picture
		
def show_catalog(request):
	goods_count=12
	goods = Good.objects.all()
	
	table = []
	for good in goods:

		item = Item()
		
		item.good = good
		
		images = Picture.objects.get(good=good, main_image=True)
		
		item.image = images 
		 	
		table.append(item)	

	page_number = request.GET.get('page', 1)

	paginator = Paginator(table, goods_count)	

	page = paginator.get_page(page_number)


	is_paginated = page.has_other_pages()

	if page.has_previous():
		prev_url = '?page={}'.format(page.previous_page_number())
	else:
		prev_url = ''	

	if page.has_next():
		next_url = '?page={}'.format(page.next_page_number())
	else:
		next_url = ''			

	template_name = '*'
	context = {
		'page_object': page, 'prev_url': prev_url, 'next_url': next_url, 'is_paginated': is_paginated,
	}
	return render(request, template_name, context)


def show_good(request, slug):
	good = Good.objects.get(slug=slug)

	pictures = Picture.objects.filter(good=good).order_by('-main_image')
	main_pictures = pictures[0]

	template_name = '*'
	context = {
		'good': good, 'pictures': pictures, 'main_pictures': main_pictures,
	}
	return render(request, template_name, context)	
