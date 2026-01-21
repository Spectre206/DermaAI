from django.urls import path
from .views import PredictSkinDiseaseView, PatientHistoryView, SubmitFeedbackView

urlpatterns = [
    path('predict/', PredictSkinDiseaseView.as_view(), name='predict-skin-disease'),
    path('history/', PatientHistoryView.as_view(), name='patient-history'),
    path('feedback/', SubmitFeedbackView.as_view(), name='submit-feedback'),
]