from django.contrib.auth.models import AbstractUser
from django.db import models

class User(AbstractUser):
    is_active = models.BooleanField(default=True)
    
class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6)
    
    def __str__(self):
        return f"Confirmation code for {self.user.username}"