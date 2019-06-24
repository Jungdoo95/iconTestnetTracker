from django.db import models

# Create your models here.
class area(models.Model):
    idx = models.AutoField(primary_key=True)    
    title = models.CharField(max_length=30)
<<<<<<< HEAD
    titleBG = models.CharField(max_length=100, blank=True)
    titleColor = models.CharField(max_length=30, blank=True)
    path = models.TextField(blank=True)
    bodyBG= models.CharField(max_length=30, blank=True)
    bodyColor = models.CharField(max_length=30, blank=True)
    img_src = models.CharField(max_length=100)
    ellipsis = models.CharField(max_length=100)
    jibun = models.CharField(max_length=100)
    link = models.CharField(max_length=100, blank=True)
    regDate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}, {}'.format(self.title ,self.regDate)
=======
    titleBG = models.CharField(max_length=30)
    titleColor = models.CharField(max_length=30)
    path = models.TextField()
    bodyBG= models.CharField(max_length=30)
    bodyColor = models.CharField(max_length=30)
    img_src = models.CharField(max_length=100)
    ellipsis = models.CharField(max_length=100)
    jibun = models.CharField(max_length=100)
    link = models.CharField(max_length=100)
    regDate = models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return '{}, {}'.format(self.name ,self.regDate)
>>>>>>> b9adcce0e6e1a246ccd7455f54d68b0a8efb7ee8
