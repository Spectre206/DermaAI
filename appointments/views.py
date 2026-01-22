from rest_framework import generics, filters
from django_filters.rest_framework import DjangoFilterBackend
import django_filters  
from rest_framework.permissions import IsAuthenticated, AllowAny
from .models import Doctor, Appointment
from .serializers import DoctorSerializer, AppointmentSerializer

# --- CUSTOM FILTER SET ---
class DoctorFilter(django_filters.FilterSet):
    # This enables "fuzzy" matching (e.g., "peshawar" matches "Peshawar")
    city = django_filters.CharFilter(field_name='city', lookup_expr='icontains')
    
    # We map the URL parameter 'specialty' to the model field 'specialty'
    
    specialty = django_filters.CharFilter(field_name='specialty', lookup_expr='icontains')

    class Meta:
        model = Doctor
        fields = ['city', 'specialty']

# --- 1. HOME SCREEN API (Public) ---
class DoctorListView(generics.ListAPIView):
    """
    Returns a list of doctors with advanced filtering.
    """
    queryset = Doctor.objects.filter(is_available=True)
    serializer_class = DoctorSerializer
    permission_classes = [AllowAny]
    
    # 1. Enable the Filter Backend
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    
    # 2. Link our Custom Filter Class
    filterset_class = DoctorFilter
    
    # 3. Enable General Search (e.g. ?search=Ali)
    search_fields = ['name', 'hospital_name', 'specialty']

# --- 2. BOOKING API (Private) ---
class BookAppointmentView(generics.CreateAPIView):
    queryset = Appointment.objects.all()
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated] 

# --- 3. MY APPOINTMENTS API (Private) ---
class MyAppointmentListView(generics.ListAPIView):
    serializer_class = AppointmentSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Appointment.objects.filter(patient=self.request.user)