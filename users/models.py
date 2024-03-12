# users/models.py
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AbstractUser, User
from django.db import models

class CustomUser(AbstractUser):
    wallet_balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    groups = models.ManyToManyField('auth.Group', related_name='user_custom')
    user_permissions = models.ManyToManyField('auth.Permission', related_name='user_custom')
# events/models.py




class Event(models.Model):
    organizer = models.ForeignKey(get_user_model(), on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    ticket_price = models.DecimalField(max_digits=10, decimal_places=2)
    ticket_quantity = models.IntegerField(default=0)

    def __str__(self):
        return self.name

class Wallet(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)

class Transaction(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    timestamp = models.DateTimeField(auto_now_add=True)
    transaction_type = models.CharField(max_length=20)  # 'Top Up', 'Purchase', 'Withdrawal'