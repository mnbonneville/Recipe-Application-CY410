# Generated by Django 2.0.2 on 2018-04-25 15:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cards', '0004_recipe_upload'),
    ]

    operations = [
        migrations.AddField(
            model_name='recipe',
            name='author',
            field=models.CharField(default='DEFAULT_NAME', max_length=200),
        ),
    ]
