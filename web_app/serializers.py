from rest_framework import serializers
from .models import SkinLesionScan, Feedback

class PredictionSerializer(serializers.Serializer):
    # The image field
    image = serializers.ImageField()

    def validate_image(self, value):
        if value.size > 5 * 1024 * 1024:
            raise serializers.ValidationError("Image file too large (> 5mb)")
        return value

class SkinScanSerializer(serializers.ModelSerializer):
    class Meta:
        model = SkinLesionScan
        fields = [
            'id', 'image', 'heatmap_image', 'prediction', 'confidence', 'created_at'
        ]

class FeedbackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feedback
        fields = [
            'id', 'subject', 'message', 'rating', 'created_at'
        ]