from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class UserModel(AbstractUser):
    username = None
    last_login=None
    first_name=None
    last_name=None
    accountnumber=models.IntegerField(null=False,unique=True)
    accountname=models.CharField(max_length=30,null=False)
    accountbalance=models.DecimalField(max_digits=13,decimal_places=2,null=False)
    password=models.CharField(max_length=30,null=False,default=None)

    USERNAME_FIELD='accountnumber'
    REQUIRED_FIELDS=['accountname','accountbalance']