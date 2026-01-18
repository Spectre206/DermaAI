from django.urls import path
from .views import DoctorListView, BookAppointmentView, MyAppointmentListView

urlpatterns =[
    # Home Screen 
    path('doctors/', DoctorListView.as_view(), name= 'doctor-list'),

    # Booking
    path('book/', BookAppointmentView.as_view(), name= 'book-appointment'),

    # Dashboard
    path('my-appointments/', MyAppointmentListView.as_view(), name= 'my-appointments'),

]