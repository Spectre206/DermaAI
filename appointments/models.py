from django.db import models
from django.conf import settings
from .fields import EncryptedTextField  

class Doctor(models.Model):
    class Specialty(models.TextChoices):
        DERMATOLOGIST = 'DERMATOLOGIST', 'Dermatologist'
        ALLERGIST = 'ALLERGIST', 'Allergist'
        SURGEON = 'SURGEON', 'Plastic Surgeon'
        GP = 'GP', 'General Practitioner'
        ONCOLOGIST = 'ONCOLOGIST', 'Oncologist'

    name = models.CharField(max_length=100, db_index=True)
    specialty = models.CharField(max_length=50, choices=Specialty.choices, db_index=True)
    hospital_name = models.CharField(max_length=100)
    city = models.CharField(max_length=50, db_index=True)
    is_available = models.BooleanField(default=True, db_index=True)
    qualification = models.CharField(max_length=100, help_text="e.g., MBBS, FCPS")
    experience_years = models.PositiveIntegerField(default=1)

    class Meta:
        ordering = ['name']
        indexes = [
            models.Index(fields=['specialty', 'city']),
            models.Index(fields=['specialty', 'is_available']),
        ]

    def __str__(self):
        return f"Dr. {self.name} - {self.get_specialty_display()}"


class Appointment(models.Model):
    class Status(models.TextChoices):
        PENDING = 'PENDING', 'Pending'
        CONFIRMED = 'CONFIRMED', 'Confirmed'
        COMPLETED = 'COMPLETED', 'Completed'
        CANCELLED = 'CANCELLED', 'Cancelled'

    # Using settings.AUTH_USER_MODEL
    patient = models.ForeignKey(
        settings.AUTH_USER_MODEL, 
        on_delete=models.CASCADE, 
        related_name='appointments'
    )
    doctor = models.ForeignKey(
        Doctor, 
        on_delete=models.CASCADE, 
        related_name='appointments'
    )

    date_time = models.DateTimeField(db_index=True)
    status = models.CharField(max_length=20, choices=Status.choices, default=Status.PENDING)

    # --- Using our Custom Encryption Field ---
    symptoms = EncryptedTextField(blank=True)
    ai_diagnosis = EncryptedTextField(blank=True)
    doctor_notes = EncryptedTextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date_time']
        indexes = [
            models.Index(fields=['doctor', 'date_time']),
            models.Index(fields=['patient', 'date_time']),
        ]
        constraints = [
            models.UniqueConstraint(
                fields=['doctor', 'date_time'],
                name='unique_doctor_appointment_time'
            )
        ]

    def __str__(self):
        return f"{self.patient} -> Dr. {self.doctor.name} ({self.date_time})"