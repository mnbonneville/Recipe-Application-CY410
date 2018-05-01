from django.shortcuts import render, render_to_response, redirect
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic import ListView, DetailView
from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from .models import Cart
from .models import RecipeOrder
from django.contrib import messages

from . models import Recipe
from django.urls import reverse_lazy
from django.views import generic
import paypalrestsdk
from paypalrestsdk import Payment
from django.utils import timezone

from .forms import RecipeForm

# Create your views here.

def index(request):
    #return HttpResponse("Hello, world. This is a list of recipe cards.")
    return render_to_response('index.html')

class AboutPageView(TemplateView):
    template_name = 'about.html'

class RecipeListView(ListView):
    model = Recipe
    template_name = 'home.html'

class RecipeDetailView(DetailView):
    model = Recipe
    template_name = 'recipe_detail.html'

class RecipePost(generic.CreateView):
    model = Recipe
    form_class = RecipeForm
    success_url = reverse_lazy('home')
    template_name = 'recipe_post.html'

def add_to_cart(request,recipe_id):
    recipe = get_object_or_404(Recipe, pk=recipe_id)
    cart,created = Cart.objects.get_or_create(user=request.user,active=True)
    order,created = RecipeOrder.objects.get_or_create(recipe=recipe,cart=cart)
    order.save()
    messages.success(request, "Cart updated!")
    return redirect('cart')

def remove_from_cart(request, recipe_id):
    try:
        recipe = Recipe.objects.get(pk = recipe_id)
    except ObjectDoesNotExist:
        pass
    else:
        cart = Cart.objects.get(user = request.user, active = True)
        care.remove_from_cart(recipe_id)
    return redirect('cart')

def cart(request):
    cart = Cart.objects.get(user=request.user.id, active = True)
    orders = RecipeOrder.objects.filter(cart=cart)
    total  = 0
    #count = 0
    for order in orders:
        total += order.recipe.price
    
    context = {
        'cart': orders,
        'total': total,
    }
    return render(request, 'cart.html', context)

# PAYMENT PROCESSORS

#Paypal
@login_required
def checkout(request,processor):
    cart=Cart.objects.get(user=request.user.id, active=True)
    orders= RecipeOrder.objects.filter(cart=cart)
    if processor == "paypal":
        redirect_url = checkout_paypal(request,cart,orders)
        return redirect(redirect_url)
           
    else:
        return redirect('list')

@login_required
def process_order(request,processor):
    if processor == "paypal":
        payment_id= request.GET.get('paymentId')
        cart= Cart.objects.get(payment_id=payment_id)
        orders= RecipeOrder.objects.filter(cart=cart)
        total=0
        for order in orders:
            total +=(order.recipe.price)
        context= {
            'cart': orders,
            'total': total,
        }
        return render(request, 'process_order.html', context)

@login_required
def complete_order(request,processor):
    cart= Cart.objects.get(user=request.user.id,active=True)
    if processor == "paypal":
        payment= paypalrestsdk.Payment.find(cart.payment_id)
        if payment.execute({"payer_id": payment.payer.payer_info.payer_id}):              
            message= "Success! Your order has been completed, and is being processed. Payment id: %s" %(payment.id)
            cart.active =False
            cart.order_date= timezone.now()
            cart.save()
        else:
            message = "There was a problem with the transaction. Error: %s" % (payment.error.message)
        context = {
            'message': message,
        }
        return render (request, 'order_complete.html',context)

@login_required
def order_error(request):
    return render(request, 'order_error.html')

@login_required   
def checkout_paypal(request,cart,orders):
    items = []
    total=0
    for order in orders:
        total += (order.recipe.price)
        recipe= order.recipe
        item= {
            'name': recipe.title,
            'price': str(recipe.price),
            'currency': 'USD',
            'quantity': 1
        }
        items.append(item)

    paypalrestsdk.configure({
        "mode": "sandbox",
        "client_id": ENTER OWN,
        "client_secret": ENTER OWN,
    })
   
    payment = Payment({
    "intent": "sale",

    # Payer: A resource representing a Payer that funds a payment
    # Payment Method as 'paypal'
    "payer": {
        "payment_method": "paypal"},

    # Redirect URLs
    "redirect_urls": {
        "return_url": "http://localhost:8000/cards/process/paypal",
        "cancel_url": "http://localhost:8000/cards/home"},
   
    # Transaction
    "transactions": [{

        # ItemList
        "item_list": {
            "items": items},

        # Amount
        # Let's you specify a payment amount.
        "amount": {
            "total": str(total),
            "currency": "USD"},
        "description": "This is the payment transaction description."}]})

# Create Payment and return status
    if payment.create():
        cart_instance = cart
        cart_instance.payment_id= payment.id
        cart_instance.save()
                   
        print("Payment[%s] created successfully" % (payment.id))
        # Redirect the user to given approval url
        for link in payment.links:
            if link.method == "REDIRECT":
                redirect_url = str(link.href)
                print("Redirect for approval: %s" % (redirect_url))
                return redirect_url
    else:
        print("Error while creating payment:")
        print(payment.error)
