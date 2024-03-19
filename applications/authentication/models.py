from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from .manager import CustomUserManager


def upload_to(instance, filename):
    print("\n \n inside upload_to function")
    print(instance.profile_img)
    print(filename)
    return 'profile_images/' + filename

class CustomUser(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=50)
    last_name = models.CharField(max_length=30)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=128)
    profile_img = models.ImageField(upload_to=upload_to, blank=True)
    birthdate = models.DateField(null=True)
    card_number = models.TextField(max_length=15, null=True, blank=True, unique=True)
    solde = models.IntegerField(default=5000, blank=True)
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


from django.db import models

class UploadedFile(models.Model):
    file = models.FileField(upload_to="images", blank=True)
    description = models.CharField(max_length=200, null=True, blank=True)
    uploaded_on = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.uploaded_on.strftime('%Y-%m-%d %H:%M:%S')

    def get_file_url(self):
        return self.file.url
