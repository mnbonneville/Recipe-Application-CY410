from django.urls import path
from . import views

urlpatterns = [
    path('signup/', views.ChefSignUp.as_view(), name='signup'),
]
