from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone
from datetime import date

class User(AbstractUser):
    # ... existing fields ...
    
    # Add birthday field
    birth_date = models.DateField(null=True, blank=True)
    
    @property
    def is_adult(self):
        """Check if user is at least 18 years old"""
        if not self.birth_date:
            return False
        today = date.today()
        age = today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))
        return age >= 18
    
class ConfirmationCode(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='confirmation_code')
    code = models.CharField(max_length=6)
    
    def __str__(self):
        return f"Confirmation code for {self.user.username}"