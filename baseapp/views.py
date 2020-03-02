from django.shortcuts 	import render
from django.http 		import HttpResponse

def show_index(request):
	
	return HttpResponse('hello world')
