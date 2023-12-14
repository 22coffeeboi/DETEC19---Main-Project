from django.db import models


class BaseModel(models.Model):
    objects = models.Manager()
    class Meta:
        abstract = True


class Users(models.Model):

    username = models.CharField(max_length=50 , default="")
    pass1 = models.CharField(max_length=50 , default="")


    def __str__(self):
        return self.username


#if making changes, PLEASE MIGRATE

class Predict(models.Model):
    #user = models.ForeignKey(Users,on_delete=models.CASCADE)
    result = models.CharField(max_length=100)
    img = models.FileField(default="")
    accuracy = models.IntegerField(default=0)
    #datetime = models.DateTimeField(auto_now_add=True)
    #time = models.DateTimeField(auto_now=True)

    #class Meta:
        #ordering = ["time"]



