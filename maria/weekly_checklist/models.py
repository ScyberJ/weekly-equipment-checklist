from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.conf import settings


# Custom class for managing custom user model
class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **other_fields):
        user: User = self.model(
            email=self.normalize_email(email),
            username=other_fields['username'],
        )

        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, email, password=None,  **other_fields):
        user = self.create_user(
            email=email,
            username=other_fields['username'],
            password=password,
        )
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

class User(AbstractUser):
    branch = models.ForeignKey("Branch", on_delete=models.SET_NULL, null=True, blank=True)
    objects = CustomUserManager()

    def __str__(self) -> str:
        return f"{self.username} ({self.email})"

            

class Branch(models.Model):
    code = models.IntegerField(primary_key=True)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ['name']
    
    def __str__(self) -> str:
        return f"{self.name} ({self.code})"

class Equipment(models.Model):
    serial_number = models.CharField(max_length=400, primary_key=True)
    description = models.TextField(max_length=512)
    model = models.ForeignKey("EquipmentModel", on_delete=models.SET_NULL, null=True, related_name='equipment')
    request = models.ForeignKey("Request", on_delete=models.CASCADE, related_name='equipment')

    class Meta:
        ordering = ['model', 'serial_number']

    def __str__(self) -> str:
        return f"{self.model} ({self.serial_number})"

class EquipmentModel(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name} ({self.id})"

class RequestStatus(models.TextChoices):
    INACTIVE = ('Inactive', 'Inactive')
    PENDING = ('Pending', 'Pending')
    FIXED = ('Fixed', "Fixed")

class Request(models.Model):
    reference = models.AutoField(primary_key=True)
    requested_at = models.DateTimeField(auto_now_add=True)
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE) 
    status = models.CharField(max_length=255, choices=RequestStatus.choices, default=RequestStatus.INACTIVE)

    class Meta:
        ordering = ['-requested_at']