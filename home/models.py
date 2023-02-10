from django.db import models

# Create your models here.
class Form(models.Model):
    keyword = models.CharField(max_length=120, null=True)
    size = models.CharField(max_length=3, null=True)
    duration = models.CharField(max_length=2, null=True)
    email = models.CharField(max_length=100, null=True)
    #file = models.FileField(upload_to='uploads', default=None, null=True)
    
    def __str__(self):
        return self.keyword