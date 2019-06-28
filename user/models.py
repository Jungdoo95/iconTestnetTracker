from django.db import models
from django.db.models.fields.related import ManyToManyField

# Create your models here.
class User(models.Model):
    idx = models.AutoField(primary_key=True)    
    email = models.CharField(max_length=100)
    walletAddress = models.CharField(max_length=200, blank=True)
    name = models.CharField(max_length=30, blank=True)
    nickName = models.CharField(max_length=30, blank=True)
    avatar = models.CharField(max_length=100, blank=True)
    phoneNumber = models.CharField(max_length=50, blank=True)
    lastAccess = models.DateTimeField(auto_now_add=True)
    regDate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}, {}'.format(self.email ,self.lastAccess)

    def to_dict(self):
        opts = self._meta
        data = {}
        for f in opts.concrete_fields + opts.many_to_many:
            if isinstance(f, ManyToManyField):
                if self.pk is None:
                    data[f.name] = []
                else:
                    data[f.name] = list(f.value_from_object(self).values_list('pk', flat=True))
            else:
                data[f.name] = f.value_from_object(self)
        return data