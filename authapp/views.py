from django.shortcuts import render, redirect

from django.http 					import HttpResponse
from django.http 					import HttpResponseRedirect

from django.contrib.auth.models		import User
from django.contrib.auth.forms 		import AuthenticationForm
from django.contrib					import messages

from django.contrib		 			import auth
from .forms 						import RegistrationForm
from authapp.models 				import Buyer


def show_account(request):

	context = {

	}

	template_name = '*.html'

	buyer = Buyer.objects.filter(user=request.user).first()
	
	if buyer is not None:
		
		context.update({'buyer': buyer})

	return render(request, template_name, context)


def login_register(request):


	template_name = '*.html'
	
	return render(request, template_name)

def login(request):

	if request.method == 'POST':
		form 			= AuthenticationForm(request, request.POST)

		username 		= form.data.get('username')
		password 		= form.data.get('password')

		user 			= auth.authenticate(username=username, password=password)

		if user is not None:

			auth.login(request, user)
			return render(request, '*.html')

		else:
			messages.info(request, 'Вы ввели не существующую комбинацию пароль-логин, попробуйте еще раз!')
			return redirect('')		
	
	return HttpResponseRedirect('/')

def logout(request):
	
	auth.logout(request)

	return render(request, '*.html')


def register(request):

	if request.method == 'POST':

		reg_form = RegistrationForm(request.POST)

		if reg_form.is_valid():

			userfirst_name 	= reg_form.cleaned_data['userfirst_name']
			userlast_name 	= reg_form.cleaned_data['userlast_name']
			companyname 	= reg_form.cleaned_data['companyname']
			usertel 		= reg_form.cleaned_data['usertel']
			username 		= reg_form.cleaned_data['username']
			useremail 		= reg_form.cleaned_data['useremail']
			userpassword 	= reg_form.cleaned_data['userpassword']
			userpassword_2 	= reg_form.cleaned_data['userpassword_2']

			if userpassword==userpassword_2:
				if User.objects.filter(username=username).exists():
					messages.info(request, 'Пользователь с таким именем существует!!!')
					return redirect('*')
				elif User.objects.filter(email=useremail).exists():				
					messages.info(request, 'Пользователь с таким email существует!!!')
					return redirect('*')
				else:
					user = User.objects.create_user(username=username, password=userpassword, email=useremail)
					user.save()

					new_buyer		= Buyer(user=user, first_name=userfirst_name, last_name=userlast_name, Phone=usertel, email=useremail, name=companyname)
					new_buyer.save()

					auth.login(request, user)

					template_name = '*'

					return render(request, template_name)	
			else:
				messages.info(request, 'Пароли не совпадают!!!')
				return redirect('*')			
	else:

		return redirect('*')