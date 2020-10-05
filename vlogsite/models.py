from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class VlogType(models.Model):
    type_name = models.CharField(max_length=15)

    def __str__(self):
        return self.type_name
    def natural_key(self):
        return self.__str__()

class vlogText(models.Model):
    title = models.CharField(max_length=50)
    blog_type = models.ForeignKey(VlogType,on_delete=models.DO_NOTHING)
    content =models.TextField()
    author = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    create_time = models.DateTimeField(auto_now=True)
    last_updated_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title

class comment(models.Model):
    comt = models.TextField()
    belond = models.ForeignKey(vlogText, on_delete=models.DO_NOTHING)
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    date = models.DateTimeField(auto_now=True)

    root = models.ForeignKey('self', null=True, blank=True, related_name='lof', on_delete=models.DO_NOTHING, default=None)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='father', on_delete=models.DO_NOTHING, default=None)
    def __str__(self):
        return self.comt

class geton(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    time = models.DateField(auto_now=True)
    Is_sign = models.BooleanField()

