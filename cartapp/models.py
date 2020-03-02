from django.db import models
from django.conf import settings
from goodapp.models import Good

def calculate_cart_summ(act_cart):

	items = Cart_Item.objects.filter(cart = act_cart)
	summ = 0
	for item in items:
		summ += item.summ
	act_cart.cart_summ = summ	
	act_cart.save()


class Cart(models.Model):
	cart_summ	= models.DecimalField('Сумма заказа', default = 0, blank = True, max_digits = 15, decimal_places = 0, editable = False)
	user 		= models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, null=True, blank=True)	

	def __str__(self):
		return str(self.id)

class Cart_Item(models.Model):
	cart 		= models.ForeignKey(Cart, on_delete = models.CASCADE)
	good 		= models.ForeignKey(Good, on_delete = models.PROTECT)
	quantity	= models.DecimalField(max_digits = 15, decimal_places = 0)
	price		= models.DecimalField(max_digits = 15, decimal_places = 0)
	summ		= models.DecimalField(max_digits = 15, decimal_places = 0)


	def __str__(self):
		return str(self.id)

	def save(self, *args, **kwargs):

		self.summ = self.quantity * self.price

		super(Cart_Item, self).save(*args, **kwargs)

		calculate_cart_summ(self.cart)	