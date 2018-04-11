from django.urls import path
from django.conf.urls import url

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('about/', views.AboutPageView.as_view(), name='about'),
    path('home/', views.RecipeListView.as_view(), name='home'),
    path('post/', views.RecipePost.as_view(), name='recipe_post'),
    path('recipe/<int:pk>/', views.RecipeDetailView.as_view(), name='recipe_detail'),
    url(r'^add/(\d+)$', views.add_to_cart, name='add_to_cart'),
    url(r'^remove/(\d+)$', views.remove_from_cart, name='remove_from_cart'),
    url(r'^cart/', views.cart, name='cart'),
    url(r'^checkout/(\w+)', views.checkout, name='checkout'),
    url(r'^process/(\w+)', views.process_order, name='process'),
    url(r'^order_error/', views.order_error, name='order_error'),
    url(r'^complete_order/(\w+)', views.complete_order, name='complete_order'),
]
