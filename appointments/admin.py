from django.contrib import admin
from .models import Doctor, Appointment

@admin.register(Doctor)
class DoctorAdmin(admin.ModelAdmin):
    """
    Admin View for Doctors
    ----------------------
    - Displays key info (Name, Specialty, City, Availability) in the list view.
    - filtering: Allows side-bar filtering by Specialty, Availability, and City.
    - search: Enables searching by Name, Hospital, or Qualification.
    - editable: The 'is_available' toggle can be switched directly from the list.
    - pagination: Limits results to 20 per page for better performance.
    """
    list_display = ('name', 'specialty', 'city', 'hospital_name', 'is_available', 'experience_years')
    list_filter = ('specialty', 'is_available', 'city')
    search_fields = ('name', 'hospital_name', 'qualification')
    list_editable = ('is_available',)
    list_per_page = 10

@admin.register(Appointment)
class AppointmentAdmin(admin.ModelAdmin):
    """
    Admin View for Appointments
    ---------------------------
    - Displays: Patient, Doctor, Time, Status, and Creation date.
    - filtering: Filter by Status (e.g., Pending/Confirmed) and Date.
    - search: Search functionality looks up 'patient__username' AND 'doctor__name'.
    - hierarchy: Adds a date-based navigation bar to drill down into specific months/days.
    - read-only: 'created_at' is immutable to preserve audit integrity.
    - Note: Encrypted fields (symptoms, diagnosis) are automatically decrypted
      by our custom field logic for display here.
    """
    list_display = ('patient', 'doctor', 'date_time', 'status', 'created_at')
    list_filter = ('status', 'date_time')
    search_fields = ('patient__username', 'doctor__name')
    date_hierarchy = 'date_time'
    readonly_fields = ('created_at',)