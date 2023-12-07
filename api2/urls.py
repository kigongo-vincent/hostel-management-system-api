from django.urls import path 
from . import views

from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
urlpatterns = [
    # logging in and session management
    path('token/', views.CustomTokenObtainPairView.as_view()),
    path('token/refresh', TokenRefreshView.as_view()),
    path('', views.homepage, name="home"),
    # hostels information (adding and retrieving)
    # path('hostels/',views.getHostels, name ="hostels" ),
    # creating and viewing user accounts
    path('users/<str:pk>',views.getUsers, name ="users" ),
    path('getHostels/', views.getHostels),
    path('asearch/', views.advancedSearch),
    path('getRooms/<str:pk>', views.getRooms, name="rooms"),
    path('feedback/<str:pk>', views.feedback),
    path('myreservations/<str:pk>', views.getMyReservations),
    path('Hostel/<str:pk>', views.updateHostel),
    path('myHostel/<str:pk>', views.myHostel),
    path('getUser/<str:pk>', views.getUser),
    path('getReservations/<str:pk>', views.getReservations)
]