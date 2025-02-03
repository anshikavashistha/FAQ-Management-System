from django.urls import path
from .views import get_faqs

urlpatterns = [
    path('', get_faqs),  # Remove 'api/faqs/' from here
]
