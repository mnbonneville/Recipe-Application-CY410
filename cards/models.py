from django.db import models
from datetime import date
from django.contrib.auth.models import User
from django.conf import settings
#from encrypted_model_fields.fields import EncryptedCharField
#from fernet_fields import EncryptedTextField

# Create your models here.
class Recipe(models.Model):
    title = models.CharField(max_length=200)
    body = models.TextField()
    date = models.DateField(default=date.today)
    price= models.DecimalField(decimal_places=2, max_digits=8, default=0.00)
    #sensitive = EncryptedTextField(max_length=100)

    def __str__(self):
        return self.title

class Cart(models.Model):
        user=models.ForeignKey( settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
        active=models.BooleanField(default=True)
        order_date=models.DateField(null=True)
        payment_type=models.CharField(max_length=100, null=True)
        payment_id=models.CharField(max_length=100, null=True)
        def remove_from_cart(self,recipe_id):
                recipe = Recipe.objects.get(pk=recipe_id)
                try:
                    preexisting_order = RecipeOrder.objects.get(recipe=recipe, cart = self)
                    preexisting_order.delete()
                except RecipeOrder.DoesNotExist:
                        new_order = RecipeOrder.objects.create(recipe=recipe, cart = self,)
                        
                        new_order.save()

class RecipeOrder(models.Model):
        recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)
        cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
