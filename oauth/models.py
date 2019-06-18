from django.db import models

# Create your models here.
class Users(models.Model):
    idx = models.AutoField(primary_key=True)
    loginType = models.CharField(max_length=10)
    code = models.CharField(max_length=50)
    email = models.CharField(max_length=100)
    walletAddress = models.CharField(max_length=200)
    name = models.CharField(max_length=30)
    phoneNumber = models.CharField(max_length=50)
    lastAccess = models.DateTimeField(auto_now_add=True)
    regDate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}, {}'.format(self.email ,self.lastAccess)