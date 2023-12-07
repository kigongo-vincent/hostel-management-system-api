from turtle import mode
from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    created = models.DateTimeField(auto_now_add=True)
    email = models.EmailField(unique=True, blank=False, null=False)
    photo = models.FileField(upload_to="static/profilePics",null=True, blank=True )
    contact = models.CharField(max_length=15)
    address =models.CharField(max_length=100)
    username = models.CharField(max_length=100, default="none", unique=False)
    USERNAME_FIELD ="email"
    REQUIRED_FIELDS = []

class Hostel(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    name= models.CharField(max_length=100) 
    status = models.CharField(max_length=100, default="pending")
    photo = models.FileField(upload_to="static/hostelPics", null=True)
    video = models.FileField(upload_to="static/hostelVideos", null=True)
    address = models.CharField(max_length=100)
    contact = models.CharField(max_length=15) 
    manager = models.OneToOneField(User, related_name="manager", on_delete=models.CASCADE)   
    rating = models.DecimalField(decimal_places=0, max_digits=1, default=0)
    hostel_type = models.CharField(max_length=100, null=True,blank=True)
    class Meta:
        ordering = ['-created']

    def __str__(self):
        return self.name
class Room(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    number = models.CharField(max_length=10, unique=True) 
    price = models.DecimalField(decimal_places=0, max_digits=4000000) 
    image0 = models.FileField(upload_to="static/roomPics", null=True, blank=True)
    image1 = models.FileField(upload_to="static/roomPics", null=True, blank=True)
    image2 = models.FileField(upload_to="static/roomPics", null=True, blank=True) 
    image3 = models.FileField(upload_to="static/roomPics", null=True, blank=True) 
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    occupants =models.ManyToManyField(User, related_name="occupants",blank=True)
    capacity = models.DecimalField(decimal_places=0, max_digits=1)

    def __str__(self):
        return self.number

class Reservation(models.Model):
    student = models.ForeignKey(User,on_delete=models.SET_NULL, null=True)
    room = models.ForeignKey(Room, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    amount = models.DecimalField(decimal_places=2, default=0, max_digits=10000000)
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE, default=0)
    created = models.DateTimeField(auto_now_add=True)


    class Meta:
        ordering = ['-created']
    def __str__(self):
        return self.room.number
    

class Feedback(models.Model):
    student = models.ForeignKey(User,on_delete=models.CASCADE)
    body= models.TextField()
    hostel = models.ForeignKey(Hostel, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=1, decimal_places=0)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.rating)
