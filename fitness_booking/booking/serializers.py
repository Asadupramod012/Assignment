from rest_framework import serializers
from .models import Classes, Booking

class ClassesSerializer(serializers.ModelSerializer):
    class Meta:
        model = Classes
        fields = '__all__'

class BookingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Booking
        fields = '__all__'


class BookingInputSerializer(serializers.Serializer):
    class_id = serializers.UUIDField()
    client_name = serializers.CharField(max_length=100)
    client_email = serializers.EmailField()
