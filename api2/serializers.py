from rest_framework.serializers import ModelSerializer, CharField, EmailField, FileField
from .models import Hostel,User, Room, Feedback, Reservation
class HostelSerializer(ModelSerializer):
    class Meta:
        model= Hostel
        fields='__all__'
class UserSerializer(ModelSerializer):
    class Meta:
        model=User
        fields='__all__'
        
class RoomSerializer(ModelSerializer):
    class Meta:
        model = Room
        fields= '__all__'
class FeedbackSerializer(ModelSerializer):
    email = CharField(source='student.email', read_only=True)
    photo = FileField(source='student.photo', read_only=True)
    class Meta:
        model = Feedback
        fields= '__all__'
class ReservationSerializer(ModelSerializer):
    hname = CharField(source = "hostel.name", read_only = True)
    class Meta:
        model= Reservation
        fields='__all__'
class getReservationSerializer(ModelSerializer):
    hname = CharField(source = "hostel.name", read_only = True)
    email = CharField(source='student.email', read_only=True)
    number = CharField(source='room.number', read_only=True)
    class Meta:
        model= Reservation
        fields='__all__'
