from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Doctor, Appointment
from .serializers import DoctorSerializer, AppointmentSerializer

# --- 1. HOME SCREEN API (Public) ---
class DoctorListView(generics.ListAPIView):
    """
    Returns a list of doctors. 
    Publicly accessible (no login required to browse).
    Supports filtering by City and Specialty.
    """
    queryset = Doctor.objects.filter(is_available=True)
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny] 
    
    # Enable Search & Filtering
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['city', 'specialty']  # e.g. ?city=Peshawar
    search_fields = ['name', 'hospital_name'] # e.g. ?search=Ali

# --- 2. BOOKING API (Private) ---
class BookAppointmentView(generics.CreateAPIView):
    """
    Allows a logged-in patient to book an appointment.
    """
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated] 

# --- 3. MY APPOINTMENTS API (Private) ---
class MyAppointmentListView(generics.ListAPIView):
    """
    Shows only the appointments belonging to the logged-in user.
    """
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        # Only return appointments for the current user
        return Appointment.objects.filter(patient=self.request.user)


