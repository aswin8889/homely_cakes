from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.

class Logintbl(AbstractUser):
    usertype=models.CharField(max_length=25,null=True)

class RegistrationUser(models.Model):
    name=models.CharField(max_length=25,null=True)
    address=models.CharField(max_length=150,null=True)
    contact=models.IntegerField(null=True)
    email=models.EmailField(null=True)
    userId=models.ForeignKey(Logintbl,on_delete=models.CASCADE,null=True)

class RegistrationBaker(models.Model):
    name=models.CharField(max_length=25,null=True)
    b_name=models.CharField(max_length=25,null=True)
    profile=models.ImageField()
    address=models.CharField(max_length=150,null=True)
    contact=models.IntegerField(null=True)
    email=models.EmailField(null=True)
    bakerId=models.ForeignKey(Logintbl,on_delete=models.CASCADE,null=True)

###################### ADMIN ##################################
    


###################### BAKER ##################################


class AddCakes(models.Model):
    c_name=models.CharField(max_length=25)
    desc=models.CharField(max_length=250)
    quantity=models.CharField(max_length=25,null=True)
    image=models.ImageField()
    price=models.IntegerField()
    bakerId=models.ForeignKey(RegistrationBaker,on_delete=models.CASCADE,null=True)



class Request(models.Model):
    flavour=models.CharField(max_length=25)
    desc=models.CharField(max_length=250)
    date=models.DateField()
    time=models.TimeField()
    quantity=models.CharField(max_length=25)
    current_date=models.DateField(null=True)
    status=models.CharField(max_length=20,null=True,default='pending')
    bakerId=models.ForeignKey(RegistrationBaker,on_delete=models.CASCADE,null=True)
    userId=models.ForeignKey(RegistrationUser,on_delete=models.CASCADE,null=True)


class Booking(models.Model):

    desc=models.CharField(max_length=500,null=True)
    current_date=models.DateField(null=True)
    status=models.CharField(max_length=25,default="booking confirmed")
    userId=models.ForeignKey(RegistrationUser,on_delete=models.CASCADE,null=True)
    bakerId=models.ForeignKey(RegistrationBaker,on_delete=models.CASCADE,null=True)
    cakeId=models.ForeignKey(AddCakes,on_delete=models.CASCADE,null=True)

class Message(models.Model):
    message=models.CharField(max_length=250)
    date=models.DateField()
    requestId=models.ForeignKey(Request,on_delete=models.CASCADE,null=True)
    bookId=models.ForeignKey(Booking,on_delete=models.CASCADE,null=True)
    
class Payment(models.Model):

    name=models.CharField(max_length=50,null=True)
    current_date=models.DateField(null=True)
    status=models.CharField(max_length=25,default="sucessfull")
    userId=models.ForeignKey(RegistrationUser,on_delete=models.CASCADE,null=True)

class Feedback(models.Model):

    title=models.CharField(max_length=25)
    feedback=models.CharField(max_length=250)
    rating=models.IntegerField(null=True)
    current_date=models.DateField(null=True)
    bookId=models.ForeignKey(Booking,on_delete=models.CASCADE,null=True)

    

    

   