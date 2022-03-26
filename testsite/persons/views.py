from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, logout, login as auth_login
from django.contrib.auth.models import User
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from .models import Profile, Sympathies
from .forms import (
    LoginForm,
    UserRegistrationForm,
    ProfileForm
    )
from django.http import HttpResponse
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from .serializers import (
    ProfileSerializer,
    ProfileCreateSerializer,
    )
from rest_framework import generics, status
from rest_framework.generics import (
    ListCreateAPIView,
    RetrieveUpdateDestroyAPIView,
    CreateAPIView,
    )
from rest_framework.permissions import IsAuthenticated , AllowAny
from .license import IsOwnerProfileOrReadOnly

import base64
from io import BytesIO
from PIL import Image

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
            return render(
                request,
                'persons/registration_done.html',
                {'new_user': new_user}
                )
    else:
        user_form = UserRegistrationForm()
        profile_form = ProfileForm()
    return render(request,'persons/registration.html',{
        'user_form': user_form,
        'profile_form': profile_form
        })



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
				return HttpResponse(
                    'Не верно ведён логин или пароль',
                    content_type='text/html',
                    charset='utf-8'
                    )
		else:
			return HttpResponse(
                'Не верно ведён логин или пароль',
                content_type='text/html',
                charset='utf-8')
	form = AuthenticationForm()
	return render(
        request=request,
        template_name="persons/login.html",
        context={"login_form":form}
        )


def logout_user(request):
	logout(request)
	return redirect("index")


class ProfileAPIView(ListCreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileSerializer
    permission_classes=[IsAuthenticated]



class CreateAPIUser(CreateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileCreateSerializer
    permission_classes=[AllowAny]



class UserProfileListCreateView(ListCreateAPIView):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[IsAuthenticated]

    def perform_create(self, serializer):
        user=self.request.user
        serializer.save(user=user)


class UserProfileDetailView(RetrieveUpdateDestroyAPIView):
    queryset=Profile.objects.all()
    serializer_class=ProfileSerializer
    permission_classes=[IsOwnerProfileOrReadOnly,IsAuthenticated]



@login_required
def SympathieView(request,pk):
    # if request.method == 'POST':

        if User.objects.filter(id=pk).exists():
            сute_user = User.objects.filter(id=pk).first()

            if request.user.id == pk :
                data = {'error':'Sending sympathy to yourself'}
                return HttpResponse(data, status=status.HTTP_406_NOT_ACCEPTABLE)

            elif Sympathies.objects.filter(
                main = сute_user,
                secondary = request.user
                ).exists():
                    data = {'error':'Sympathy is already worth'}
                    return HttpResponse(data, status=status.HTTP_208_ALREADY_REPORTED)
            else:
                Sympathies.objects.create(main = сute_user  , secondary = request.user)
                data = {'right':'Allowed'}

                if Sympathies.objects.filter(
                    main = request.user,
                    secondary = сute_user
                    ).exists():
                        send_mail(
                            'Вы кому-то понравились',
                            'Вы понравились {}'.format(request.user),
                            settings.DEFAULT_FROM_EMAIL,
                            [сute_user.email],
                        )

                return HttpResponse(data, status=status.HTTP_202_ACCEPTED)
