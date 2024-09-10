from django.urls import path
from .views import DocumentCreateView

urlpatterns = [
    path('upload/', DocumentCreateView.as_view(), name='document-upload'),
]
