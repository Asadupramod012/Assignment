from django.urls import path
from .views import ClassListView, BookClassView, BookingListView

urlpatterns = [
    path('classes/', ClassListView.as_view()),
    path('book/', BookClassView.as_view()),
    path('bookings/', BookingListView.as_view()),
]
