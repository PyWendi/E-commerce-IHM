from django.db import models
from datetime import timedelta
from django.utils import timezone
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager


def upload_to(instance, filename):
    return 'profile_images/' + filename

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    profile_img = models.ImageField(upload_to=upload_to, blank=True)
    birthdate = models.DateField(null=True)
    card_number = models.CharField(max_length=15, null=True, blank=True, unique=True)
    solde = models.DecimalField(default=5000.00, max_digits=15, decimal_places=2, blank=True)
    # is_admin = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True, editable=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=True)


    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.first_name


class Notification(models.Model):
    TYPE_CHOICE = [
        ("achat", "Achat"),
        ("livraison", "Livraison"),
        ("contact", "Contact"),
    ]

    owner = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    sender = models.IntegerField(null=True) #to be updated in the frontend side
    type = models.CharField(max_length=15, choices=TYPE_CHOICE)
    purchaseId = models.IntegerField(null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    expiration_duration = models.DurationField(default=timedelta(weeks=4))
    seen = models.BooleanField(default=False)
    class Meta:
        ordering = ["-created_at"]

    def isExpired(self):
        expired_time = self.created_at + self.expiration_duration
        return expired_time <= timezone.now()


class UploadedFile(models.Model):
    file = models.FileField(upload_to="images", blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uploaded_on.strftime('%Y-%m-%d %H:%M:%S')

    def get_file_url(self):
        return self.file.url



class Contact(models.Model):

    name = models.CharField(max_length=50)
    email = models.EmailField()
    text = models.TextField()

    def __str__(self):
        return self.name


