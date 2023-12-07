from django.shortcuts import render
from rest_framework.decorators import api_view,permission_classes
from rest_framework.response import Response
from rest_framework import status
from .serializers import HostelSerializer, UserSerializer, RoomSerializer, FeedbackSerializer, ReservationSerializer, getReservationSerializer
from .models import Hostel, User, Room, Feedback, Reservation
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.views import APIView
from django.core.mail import send_mail

from rest_framework_simplejwt.serializers import TokenObtainPairSerializer

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims to the token payload
        token['first_name'] = user.first_name
        token['last_name'] = user.last_name
        token['address'] = user.address
        token['contact'] = user.contact
        token['email'] = user.email
        token['photo_url'] = user.photo.url if user.photo else None
        token['groups'] = [group.name for group in user.groups.all()] 

        return token

class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer
@api_view(['GET'])
def getUser(request,pk):
    print(request)
    try:
        user = User.objects.get(id=pk)
        converted = UserSerializer(user)
        return Response(converted.data)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)
@api_view(['GET', 'POST'])
def getUsers(request,pk):
    users = User.objects.all()

    # try:
    if request.method == "POST":
            
            

            # assign a user to a group
         
            if pk== "student":
                group = Group.objects.get(name="student")
            elif pk == "manager":
                group = Group.objects.get(name="manager")
            elif pk == "dean":
                group = Group.objects.get(name="dean")

            # creating a new user in the db
            user=UserSerializer(data=request.data)
            if user.is_valid():
                userSave = user.save(password = make_password(request.data['password']))
                try:
                    send_mail("account creation", f"An account was created on our Hostel booking system, your email for logging in is, {request.data['email']}, and your password is {request.data['password']}", 'kigongovincent81@gmail.com', [request.data['email']])
                    group.user_set.add(userSave.id)
                    return Response(user.data, status=status.HTTP_201_CREATED)
                except Exception as e:
                    return Response({'error': str(e)}, status=500)
            
    # except:
    #     return Response(status=status.HTTP_400_BAD_REQUEST)
    converted = UserSerializer(users, many=True)
    return Response(converted.data)

# function for retrieving all hostels in the database

@api_view(['GET', 'POST'])
def getHostels(request):
    hostels = Hostel.objects.all()

    try:
        if request.method == "POST":
            converted = HostelSerializer(data=request.data)
            if converted.is_valid():
                converted.save()
                user1 = User.objects.get(id=request.data['manager'])
                dean = Group.objects.get(name = "dean").user_set.all()
                send_mail("Hostel Upload", f"You have successfully uploaded your hostel information (for {request.data['name']}), please be patient as the Dean reviews your submission", 'kigongovincent81@gmail.com', [user1.email])
                send_mail("Hostel Upload", f"You have a new hostel on the platform to approve (for {request.data['name']})", 'kigongovincent81@gmail.com', [dean[0].email])
                return Response(status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    

    converted = HostelSerializer(hostels, many =True)
    return Response(converted.data)




def homepage(request):
    return render(request, 'index.html')
#function for retrieving the rooms in the hostel




@api_view(['GET', 'POST'])
def getRooms(request,pk):
    try:
       if request.method== 'POST':
          Serialized=RoomSerializer(data=request.data)
          if Serialized.is_valid():
            Serialized.save()
            return Response(status=status.HTTP_201_CREATED)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    try:
        hostel = Hostel.objects.get(id=pk)
        rooms = hostel.room_set.all()
        convert=RoomSerializer(rooms, many= True)
    except:
       return Response(status=status.HTTP_404_NOT_FOUND)

    return Response(convert.data,status=status.HTTP_200_OK)


# information about a given hostel and making updates
@api_view(['GET', 'PATCH'])
@permission_classes([IsAuthenticated])
def updateHostel(request, pk):
    try:
        hostel = Hostel.objects.get(id=pk)
    except:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'PATCH':
        Updated = HostelSerializer(hostel, data=request.data, partial=True)
        if Updated.is_valid():
            Updated.save()
            send_mail("Account approval", f"your  hostel ({hostel.name}) has been approved successfully on the Hostel Booking System","kigongovincent81@gmail.com", [hostel.manager.email])
            return Response(Updated.data, status=status.HTTP_202_ACCEPTED)
        return Response(Updated.errors, status=status.HTTP_400_BAD_REQUEST)

    Updated = HostelSerializer(hostel)
    return Response(Updated.data)

@api_view(['GET', 'POST','PATCH'])
# @permission_classes([IsAuthenticated])
def feedback(request, pk):

    
    reviews = Feedback.objects.all()
    hostel = Hostel.objects.get(id=pk)
    if request.method == 'POST':
        converted = FeedbackSerializer(data=request.data)
        if converted.is_valid():
            converted.save()
            total =0
            if hostel is not None:
                    comments = hostel.feedback_set.all()
                    if comments is not None:
                        total = 0
                        for comment in comments:
                            total += int(comment.rating)
                        
                        Updated = HostelSerializer(hostel, data={"rating": round(total/comments.count())}, partial=True) 
                        if Updated.is_valid():
                            Updated.save()
            
        return Response(converted.data, status=status.HTTP_201_CREATED)
    try:
        reviews = hostel.feedback_set.all()
        converted= FeedbackSerializer(reviews, many=True)
        return Response(converted.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['GET','POST'])
def getReservations(request, pk):
    try:
        try:
            if request.method == 'POST':
                converted = ReservationSerializer(data=request.data)
                if converted.is_valid():
                    
                    room = Room.objects.get(id = int(request.data['room']))
                    try:
                        resident = room.occupants.all().get(id=int(request.data['student']))
                    except:  
                        resident = 0  
                    if resident == 0:
                        if room.occupants.all().count() < 3:
                            user1 = User.objects.get(id = request.data['student'])
                            room1 = Room.objects.get(id = request.data['room'])
                            hostel1 = Hostel.objects.get(id = request.data['hostel'])
                            amount = request.data['amount']
                            send_mail("Reservation", f"Your email, {user1.email} was used to make a booking for room {room1.number} in {hostel1.name} at a charge of UGX {amount}", 'kigongovincent81@gmail.com', [user1.email])
                            send_mail("Reservation", f"Account under, {user1.email} was used to make a booking for room {room1.number} in your hostel {hostel1.name} at a charge of UGX {amount}", 'kigongovincent81@gmail.com', [hostel1.manager.email])
                            
                            converted.save()

                            room.occupants.add(int(request.data['student']))
                            return Response(status=status.HTTP_201_CREATED)
                        else:
                            return Response(status=status.HTTP_226_IM_USED)
                        
                    else:
                        return Response(status=status.HTTP_304_NOT_MODIFIED)    
        except:
            return Response(status=status.HTTP_406_NOT_ACCEPTABLE)        
        hostel = Hostel.objects.get(id=pk)
        reservations = hostel.reservation_set.all()
        converted = getReservationSerializer(reservations, many=True)
        return Response(converted.data)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)

from django.http import JsonResponse
from django.core.serializers.json import DjangoJSONEncoder
from django.utils.translation import gettext_lazy as _

def getMyReservations(request, pk):
    reservations = Reservation.objects.filter(student=pk)
    reservationz = []

    for reservation in reservations:
        reservation_data = {
            "id": reservation.id,
            "number": reservation.room.number,
            "amount": reservation.amount,
            "price": reservation.room.price,
            "capacity": reservation.room.capacity,
            "occupants": reservation.room.occupants.count(),
            "created": reservation.created,
            "hname" :reservation.room.hostel.name,
            "photo_url": reservation.student.photo.url if reservation.student.photo else None,
        }

        reservationz.append(reservation_data)

    return JsonResponse(reservationz, safe=False, encoder=DjangoJSONEncoder)

from django.db.models import Q

@api_view(['GET', 'POST'])
def advancedSearch(request):
    if request.method == 'POST':
        room = Room.objects.filter(
            Q(hostel__name__icontains = request.data['name'])
            & Q(hostel__rating__icontains = str(request.data['rating']))
            &Q(price = str(request.data['price']))
            &Q(hostel__address__icontains = str(request.data['address']))
            &Q(capacity = str(request.data['capacity']))
            )
        converted = RoomSerializer(room, many =True)
        return Response(converted.data)
    return Response(status=status.HTTP_406_NOT_ACCEPTABLE)


@api_view(['GET'])
def myHostel(request, pk):
    try: 
        hostel = Hostel.objects.get(manager = pk)
    except:
        return Response(status=status.HTTP_400_BAD_REQUEST)
    converted = HostelSerializer(hostel)
    return Response(converted.data)








    

  


        
        
