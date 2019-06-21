from django.db import models

# Create your models here.
class area(models.Model):
    idx = models.AutoField(primary_key=True)    
    title = models.CharField(max_length=30)
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