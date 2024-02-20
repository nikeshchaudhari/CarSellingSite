from django.db import models
from django.contrib.auth.models import User


exposed_request = None
# Create your models here.
class Register(models.Model):
    user=models.ForeignKey(User,on_delete=models.CASCADE,null=True)
    gen=models.CharField(max_length=30,null=True)
    add=models.CharField(max_length=100,null=True)
    mobile=models.CharField(max_length=10,null=True)
    image=models.FileField(null=True)
    birth=models.DateField(null=True)
    def __str__(self):
        return self.user.username

class State(models.Model):
    state=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.state


class District(models.Model):
    state=models.ForeignKey(State,on_delete=models.CASCADE,null=True)
    dist=models.CharField(max_length=100,null=True)
    def __str__(self):
        return self.dist+" "+self.state.state





class Owner_Detail(models.Model):
    register=models.ForeignKey(Register,on_delete=models.CASCADE,null=True)
    state=models.ForeignKey(State,on_delete=models.CASCADE,null=True)
    dist=models.ForeignKey(District,on_delete=models.CASCADE,null=True)
    local_add = models.CharField(max_length=100,null=True)
    title=models.CharField(max_length=100,null=True)
    desc=models.CharField(max_length=300,null=True)
    price=models.IntegerField(null=True)
    img=models.FileField(null=True)
    brand=models.CharField(max_length=100,null=True)
    model = models.CharField(max_length=100, null=True)
    year = models.CharField(max_length=20, null=True)
    fuel = models.CharField(max_length=100, null=True)
    kmdriven = models.CharField(max_length=100, null=True)
    noofowner = models.CharField(max_length=100, null=True)
    postdate = models.DateTimeField(auto_now_add=True,null=True)

    @property
    def get_car_status(self):
        car = Status.objects.get(car = self)
        return car.status
        
    @property
    def is_favourate(self):
        fav = Favourate.objects.get(user=exposed_request.user,car_detail=self)
        return fav.favourate
        



    def __str__(self):
        return f"{self.register.user.username}-{self.brand}" 

class Status(models.Model):
    car = models.ForeignKey(Owner_Detail, on_delete=models.CASCADE,null=True,related_name='car_status')
    status = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.car}-{self.status}"

class Favourate(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE)
    car_detail = models.ForeignKey(Owner_Detail, on_delete=models.CASCADE)
    favourate = models.BooleanField(default = False)

    def __str__(self) -> str:
        return f"{self.user.username}"  

    

class Image(models.Model):
    owner=models.ForeignKey(Owner_Detail,on_delete=models.CASCADE,null=True)
    room_name=models.CharField(max_length=100,null=True)
    img=models.FileField(null=True)
    def __str__(self):
        return self.owner.register.user.username+" "+self.room_name

class Send_Feedback(models.Model):
    email= models.TextField(null=True)
    contact=models.IntegerField(null=True)
    message1 = models.TextField(null=True)

    def __str__(self):
        return self.profile.user.username



