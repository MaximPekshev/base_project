from django.db import models

from django.conf import settings

from goodapp.models import Good
from authapp.models import Buyer


class Order(models.Model):

	summ		= models.DecimalField('Сумма заказа', default = 0, blank = True, max_digits = 15, decimal_places = 0, editable = False)

	buyer 		= models.ForeignKey(Buyer, on_delete=models.CASCADE, null=True, blank=True)	

	address 	= models.CharField(max_length=1024, verbose_name='Адрес', blank=True)

	def __str__(self):
		return str(self.id)

	class Meta:
		
		verbose_name = 'Заказ'
		verbose_name_plural = 'Заказы'

class Order_Item(models.Model):
	
	order 		= models.ForeignKey(Order, on_delete = models.CASCADE)
	good 		= models.ForeignKey(Good, on_delete = models.PROTECT)
	quantity	= models.DecimalField(max_digits = 15, decimal_places = 0)
	price		= models.DecimalField(max_digits = 15, decimal_places = 0)
	summ		= models.DecimalField(max_digits = 15, decimal_places = 0)


	def __str__(self):
		return str(self.id)
