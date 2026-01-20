import os
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, generics
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from .serializers import PredictionSerializer, SkinScanSerializer
from .models import SkinLesionScan  

# Import AI Logic
from ml_engine.predictor import predict_image 

class PredictSkinDiseaseView(APIView):
    parser_classes = (MultiPartParser, FormParser)
    permission_classes = [IsAuthenticated] # User MUST be logged in to save history

    def post(self, request, *args, **kwargs):
        serializer = PredictionSerializer(data=request.data)
        
        if serializer.is_valid():
            uploaded_file = serializer.validated_data['image']
            
            # 1. Create the Database Record (Saves image to disk automatically)
            scan_record = SkinLesionScan.objects.create(
                patient=request.user,
                image=uploaded_file
            )
            
            try:
                # 2. Get the full file path from the new record
                # (e.g., D:\DermaAI\media\lesion_scans\2026\01\19\test.jpg)
                full_file_path = scan_record.image.path
                
                # 3. Call AI Brain
                result = predict_image(full_file_path)
                
                if "error" in result:
                    # If AI fails, we might want to delete the bad record
                    scan_record.delete()
                    return Response(result, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
                
                # 4. Save Results to Database
                scan_record.prediction = result['diagnosis']
                scan_record.confidence = float(result['confidence'])
                scan_record.heatmap_image = result.get('heatmap_url')
                scan_record.save()
                
                # 5. Return Response
                return Response({
                    "status": "success",
                    "scan_id": scan_record.id,
                    "prediction": scan_record.prediction,
                    "confidence": f"{scan_record.confidence}%",
                    "image_url": scan_record.image.url,
                    "heatmap_url": scan_record.heatmap_image
                }, status=status.HTTP_201_CREATED)

            except Exception as e:
                # Cleanup if logic crashes
                scan_record.delete()
                return Response({"error": f"Processing Failed: {str(e)}"}, status=500)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class PatientHistoryView(generics.ListAPIView):
    serializer_class = SkinScanSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return SkinLesionScan.objects.filter(patient=self.request.user).order_by('-created_at')
    