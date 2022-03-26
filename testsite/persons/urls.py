
from django.urls import path
from . import views
from django.urls import include


urlpatterns = [
    path('registration/', views.registration, name='registration'),
    path('login/', views.login, name='login'),
    path("logout/", views.logout_user, name= "logout"),
    path('api/clients/all', views.ProfileAPIView.as_view(), name='profile-api'),
    path('api/clients/create', views.CreateAPIUser.as_view(), name='create-api-user'),
    path('api/<int:pk>/match/', views.SympathieView, name = 'sympathie')


    ]
