from django.urls import path
from django.urls import include
from .views import show_index

urlpatterns = [
	path('', show_index, name='show_index'),
]
