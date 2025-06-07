from django.shortcuts import get_object_or_404
from rest_framework.views import APIView
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework import status
from django.http import HttpResponse
from django.utils.timezone import now
from zoneinfo import ZoneInfo
from .models import Classes, Booking
from .serializers import ClassesSerializer, BookingSerializer

# Create your views here.

class ClassListView(APIView):
    def get(self, request):
        classes = Classes.objects.all() #fetching the all classes from db
        serializer = ClassesSerializer(classes, many=True) # converting into JSON
        data = serializer.data # which is the data 
        
        return Response(data)

    # def post(self, request):
    #     serializer = ClassesSerializer(data=request.data)
    #     if serializer.is_valid():
    #         serializer.save(
    #             available_slots=serializer.validated_data['total_slots']
    #         )
    #         return Response(serializer.data, status=status.HTTP_201_CREATED)
    #     return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class BookClassView(APIView):
            
    def post(self, request):
        serializer = BookingSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        name = serializer.validated_data['client_name']
        email = serializer.validated_data['client_email']
        
        class_id = request.data.get("class_id")

        # Fix starts here
        if hasattr(class_id, 'class_id'):
            class_id = str(class_id.class_id)

        try:
            fitness_class = Classes.objects.get(class_id=class_id)
        except Classes.DoesNotExist:
            return Response({"error": "Class not found"}, status=status.HTTP_404_NOT_FOUND)

        if fitness_class.available_slots <= 0:
            return Response({"error": "No slots available"}, status=status.HTTP_400_BAD_REQUEST)

        Booking.objects.create(class_id=fitness_class, client_name=name, client_email=email)
        fitness_class.available_slots -= 1
        fitness_class.save()

        return Response({"message": "Booking confirmed"}, status=status.HTTP_201_CREATED)
    
class BookingListView(APIView):
    def get(self, request):
        email = request.GET.get('email')
        if not email:
            return Response({"error": "Email required"}, status=status.HTTP_400_BAD_REQUEST)

        bookings = Booking.objects.filter(client_email=email)
        if not bookings.exists():
            return Response({
                "message": "There is No bookings on this email (or) Dear user, plesae remove the slash after email ..."
            }, status=status.HTTP_404_NOT_FOUND)

        serializer = BookingSerializer(bookings, many=True)
        return Response(serializer.data)



#----------------------------------------------------------------------------------------

def home_view(request):
    html = """
    <html>
        <head>
            <title>Fitness Classes</title>
            <style>
                body {
                    font-family: Arial, sans-serif;
                    padding: 40px;
                    background-color: #e6f2ff;
                    color: #2c3e50;
                }
                h1 {
                    color: #005580;
                }
                p {
                    font-size: 18px;
                    margin-bottom: 30px;
                }
                .nav-link {
                    display: inline-block;
                    margin: 10px 10px 0 0;
                    padding: 10px 20px;
                    background-color: #cce0ff;
                    color: #003366;
                    text-decoration: none;
                    border-radius: 5px;
                    font-weight: bold;
                }
                .nav-link:hover {
                    background-color: #b3d1ff;
                }
            </style>
        </head>
        <body>
            <h1>Fitness Classes</h1>
            <p>Welcome to the fitness studio offering classes like <strong>Yoga</strong>, <strong>Zumba</strong>, and <strong>HIIT</strong>. Clients can view available classes and book a spot.</p>
            <a class="nav-link" href="/classes/">View Classes</a>
            <a class="nav-link" href="/book/">Book a Class</a>
            <a class="nav-link" href="/bookings/">View Bookings</a>
        </body>
    </html>
    """
    return HttpResponse(html)
