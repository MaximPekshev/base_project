from django.contrib import admin

from .models import Good
from .models import Picture



class PictureInline(admin.TabularInline):
    model = Picture
    exclude = ('title', 'slug',)
    extra = 0

class GoodAdmin(admin.ModelAdmin):
	list_display = (
					'vendor_code', 
					'name',
					'good_code',
					'slug',
					)
	
	inlines 	 = [PictureInline]

	exclude = ('slug',)

admin.site.register(Good, GoodAdmin)

class PictureAdmin(admin.ModelAdmin):
	list_display = (
					'slug', 
					'title',				
					)
	list_filter = (
					'good', 
					)
	exclude = ('slug',)

admin.site.register(Picture, PictureAdmin)