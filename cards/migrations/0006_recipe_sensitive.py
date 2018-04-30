# Generated by Django 2.0.2 on 2018-04-25 16:20

from django.db import migrations, models
import django_cryptography.fields


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0005_recipe_author'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='sensitive',
            field=django_cryptography.fields.encrypt(models.CharField(default=0.0, max_length=50)),
        ),
    ]