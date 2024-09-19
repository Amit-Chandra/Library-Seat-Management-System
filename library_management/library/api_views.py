from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.shortcuts import get_object_or_404
from .models import Library, Seat, UserProfile, Payment
from .serializers import StudentSignupSerializer, UserProfileSerializer, LibrarySerializer, SeatSerializer
from rest_framework import generics
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication
from geopy.distance import geodesic

def calculate_distance(user_location, library_location):
    return geodesic(user_location, library_location).km

# class StudentSignupAPI(APIView):
#     def post(self, request):
#         serializer = StudentSignupSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             UserProfile.objects.create(user=user, role='student')
#             return Response({'message': 'Student registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StudentSignupAPI(APIView):
    def post(self, request):
        serializer = StudentSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            # Automatically create user profile for student
            UserProfile.objects.create(user=user, role='student')
            return Response({'message': 'Student registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class StudentProfileAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         profile = get_object_or_404(UserProfile, user=request.user)
#         serializer = UserProfileSerializer(profile)
#         return Response(serializer.data)

#     def put(self, request):
#         profile = get_object_or_404(UserProfile, user=request.user)
#         serializer = UserProfileSerializer(profile, data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response({'message': 'Profile updated successfully'})
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



class StudentProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(profile)
        return Response(serializer.data)

    def put(self, request):
        profile = get_object_or_404(UserProfile, user=request.user)
        serializer = UserProfileSerializer(profile, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'message': 'Profile updated successfully'})
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class LibraryListAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         # print(f"Authorization Header: {request.headers.get('Authorization')}")
#         libraries = Library.objects.all()
#         serializer = LibrarySerializer(libraries, many=True)
#         permission_classes = [IsAuthenticated]
#         return Response(serializer.data)



class LibraryListAPI(APIView):
    permission_classes = []  # Allow unauthenticated users to access this API

    def get(self, request):
        user_lat = request.query_params.get('lat')
        user_lon = request.query_params.get('lon')

        if not user_lat or not user_lon:
            return Response({"error": "Please provide latitude and longitude."}, status=status.HTTP_400_BAD_REQUEST)

        user_location = (float(user_lat), float(user_lon))
        libraries = Library.objects.all()

        result = []
        for library in libraries:
            library_location = (library.latitude, library.longitude)  # Assuming Library model has latitude & longitude
            distance = calculate_distance(user_location, library_location)
            result.append({
                "name": library.name,
                "address": library.address,  # Assuming you have address field
                "owner": library.owner.username,  # Assuming owner is a foreign key to User
                "distance_km": distance,
                "available_seats": library.seats.filter(is_booked=False).count(),
                "total_seats": library.seats.count()
            })

        return Response(result)




class SeatAvailabilityAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, library_id):
        library = get_object_or_404(Library, id=library_id)
        seats = library.seats.all()
        serializer = SeatSerializer(seats, many=True)
        return Response({'library': library.name, 'seats': serializer.data})

class ApproveStudentAPI(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request, student_id):
        student = get_object_or_404(UserProfile, id=student_id)
        payment = Payment.objects.filter(student=student.user, is_confirmed=True).first()
        if payment:
            student.approved = True
            student.save()
            return Response({'message': 'Student approved successfully'})
        else:
            return Response({'error': 'Payment not confirmed'}, status=status.HTTP_400_BAD_REQUEST)


# ======================================================================================

class CreateLibraryAPI(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = LibrarySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RetrieveLibraryAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, library_id):
        library = get_object_or_404(Library, id=library_id)
        serializer = LibrarySerializer(library)
        return Response(serializer.data, status=status.HTTP_200_OK)


class UpdateLibraryAPI(APIView):
    permission_classes = [IsAdminUser]

    def put(self, request, library_id):
        library = get_object_or_404(Library, id=library_id)
        serializer = LibrarySerializer(library, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteLibraryAPI(APIView):
    permission_classes = [IsAdminUser]

    def delete(self, request, library_id):
        library = get_object_or_404(Library, id=library_id)
        library.delete()
        return Response({'message': 'Library deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


class ListLibrariesAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        libraries = Library.objects.all()
        serializer = LibrarySerializer(libraries, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

