from django import forms
 
class RegistrationForm(forms.Form):

	userfirst_name  = forms.CharField(max_length = 50)
	userlast_name  	= forms.CharField(max_length = 50)
	companyname 	= forms.CharField(max_length = 50)
	usertel			= forms.CharField(max_length = 50)
	username		= forms.CharField(max_length=50)
	useremail		= forms.EmailField(max_length=254)
	userpassword 	= forms.CharField(max_length = 50)
	userpassword_2 	= forms.CharField(max_length = 50)