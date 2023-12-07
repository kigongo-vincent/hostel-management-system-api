from django.contrib import admin
from .models import User, Hostel, Room, Reservation, Feedback
admin.site.register(User)
admin.site.register(Hostel)
admin.site.register(Room)
admin.site.register(Reservation)
admin.site.register(Feedback)
# Register your models here.
