# Generated by Django 5.0.3 on 2024-03-20 18:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0004_product_rate'),
    ]

    operations = [
        migrations.AlterField(
            model_name='product',
            name='rate',
            field=models.IntegerField(default=0),
        ),
    ]
