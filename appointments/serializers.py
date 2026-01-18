from rest_framework import serializers
from .models import Doctor, Appointment

class DoctorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Doctor
        fields = [
            'id', 'name', 'specialty', 'hospital_name','city',
            'is_available', 'qualification', 'experience_years'
        ]

class AppointmentSerializer(serializers.ModelSerializer):

    doctor_name = serializers.CharField(source = 'doctor.name', read_only= True)
    doctor_specialty = serializers.CharField(source= 'dotor.specialty', read_only= True)

    class Meta:
        model = Appointment
        fields = [
            'id', 'doctor', 'doctor_name', 'doctor_specialty',
            'date_time', 'status', 'symptoms', 'ai_diagnosis', 'doctor_notes'
        ]
        read_only_fields = ['status', 'ai_diagnosis', 'doctor_notes']

        
    def create(self, validated_data):
    # Automatically assign the logged-in user as the patient
        validated_data['patient'] = self.context['request'].user
        return super().create(validated_data)
