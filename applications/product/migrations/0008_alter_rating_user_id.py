# Generated by Django 5.0.3 on 2024-03-20 19:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0007_alter_rating_user_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='rating',
            name='user_id',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]