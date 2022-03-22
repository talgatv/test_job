from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout
from django.contrib.auth import login as auth_login
from .forms import LoginForm, UserRegistrationForm, ProfileForm
# from .forms import UserEditForm,
from django.contrib.auth.decorators import login_required
from .models import Profile
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from django.contrib.auth.forms import AuthenticationForm


def index(request):
    return render(request, 'index.html')


def registration(request):
    """ Регистрация """
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        profile_form = ProfileForm(request.POST, request.FILES)
        if user_form.is_valid() and profile_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.save()
            profile_user_form = profile_form.save(commit=False)
            profile_user_form.user = get_object_or_404(User, id = new_user.id )
            profile_user_form.save()
            return render(request,'persons/registration_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request,'persons/registration.html',{'user_form': user_form,'profile_form': profile_form})



def login(request):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				auth_login(request, user)
				return redirect("index")
			else:
				return HttpResponse('Не верно ведён логин или пароль', content_type='text/html', charset='utf-8')
		else:
			return HttpResponse('Не верно ведён логин или пароль', content_type='text/html', charset='utf-8')
	form = AuthenticationForm()
	return render(request=request, template_name="persons/login.html", context={"login_form":form})


def logout_user(request):
	logout(request)
	return redirect("index")
