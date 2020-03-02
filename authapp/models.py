from django.db import models

from django.conf import settings

class Buyer(models.Model):
	
	user 					= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=True)

	first_name 				= models.CharField(max_length=150, verbose_name='Имя', blank=True)
	last_name 				= models.CharField(max_length=150, verbose_name='Фамилия', blank=True)
	Phone	 				= models.CharField(max_length=150, verbose_name='Телефон', blank=True, null=True)
	email					= models.CharField(max_length=150, verbose_name='email', default='')

	address 				= models.CharField(max_length=1024, verbose_name='Адрес', blank=True)

	def __str__(self):
		
		return self.last_name


	def save(self, *args, **kwargs):
		
		super(Buyer, self).save(*args, **kwargs)


	class Meta:
		
		verbose_name = 'Заказчик'
		verbose_name_plural = 'Заказчики'
