# Generated by Django 5.0.3 on 2024-03-18 19:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('authentication', '0004_uploadedfile'),
    ]

    operations = [
        migrations.AlterField(
            model_name='uploadedfile',
            name='file',
            field=models.FileField(blank=True, upload_to='images/'),
        ),
    ]