from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.shortcuts import get_object_or_404
from geopy.distance import geodesic

from library.regular_views import library_list  # For calculating distance between two geo-locations
from .models import Library, Seat, UserProfile, Payment
from .serializers import ApproveUserSerializer, UserProfileSerializer, LibrarySerializer, SeatSerializer
from rest_framework.permissions import IsAdminUser
from rest_framework.authentication import TokenAuthentication
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
# from .models import Library, StudentProfile
from django.contrib.auth.models import User
from .serializers import LibrarySerializer, UserProfileSerializer
from rest_framework.generics import RetrieveAPIView, DestroyAPIView
from django.shortcuts import get_object_or_404


from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status
from .models import UserProfile
from .serializers import UserSignupSerializer

# ========================= Helper Function ============================
def calculate_distance(user_location, library_location):
    return geodesic(user_location, library_location).km  # Returns distance in kilometers



# class SignupAPI(generics.CreateAPIView):
#     serializer_class = UserSignupSerializer

#     def create(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.save()

#         # Create UserProfile for the new user
#         UserProfile.objects.create(
#             user=user,
#             dob=request.data.get('dob'),
#             hobbies=request.data.get('hobbies'),
#             contact_number=request.data.get('contact_number'),
#             latitude=request.data.get('latitude'),
#             longitude=request.data.get('longitude')
#         )
        
#         return Response({"message": "Student registered successfully"}, status=status.HTTP_201_CREATED)



class SignupAPI(generics.CreateAPIView):
    serializer_class = UserSignupSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        # The profile will automatically be created via the post_save signal

        # Update the UserProfile with additional fields
        user_profile = user.userprofile
        user_profile.dob = request.data.get('dob')
        user_profile.hobbies = request.data.get('hobbies')
        user_profile.contact_number = request.data.get('contact_number')
        user_profile.latitude = request.data.get('latitude')
        user_profile.longitude = request.data.get('longitude')
        user_profile.save()

        return Response({"message": "Student registered successfully"}, status=status.HTTP_201_CREATED)



# ========================= Library List API with Geo-location ============================
class LibraryListAPI(APIView):
    # Removed authentication requirement to allow public access
    def get(self, request):
        user_lat = request.query_params.get('lat')  # User's latitude
        user_lng = request.query_params.get('lng')  # User's longitude

        # Fetch all libraries
        libraries = Library.objects.all()
        library_data = []

        if user_lat and user_lng:
            user_location = (float(user_lat), float(user_lng))
            for library in libraries:
                library_location = (library.latitude, library.longitude)
                distance = calculate_distance(user_location, library_location)
                library_data.append({
                    'name': library.name,
                    'location': library.location,
                    'distance': f"{distance:.2f} km",
                    'owner': library.owner.username if library.owner else "No Owner",
                    'seat_availability': library.seats.filter(is_occupied=False).count()
                })
        else:
            # If no user location is provided, return all libraries without distance calculation
            for library in libraries:
                library_data.append({
                    'name': library.name,
                    'location': library.location,
                    'owner': library.owner.username if library.owner else "No Owner",
                    'seat_availability': library.seats.filter(is_occupied=False).count()
                })

        return Response(library_data)

# ========================= Seat Availability API ============================
class SeatAvailabilityAPI(APIView):
    def get(self, request, library_id):
        library = get_object_or_404(Library, id=library_id)
        seats = library.seats.all()
        serializer = SeatSerializer(seats, many=True)
        return Response({
            'library_name': library.name,
            'available_seats': serializer.data
        })

# ========================= Create Library API with Geo-location ============================
class CreateLibraryAPI(APIView):
    permission_classes = [IsAdminUser]

    def post(self, request):
        serializer = LibrarySerializer(data=request.data)
        if serializer.is_valid():
            # library = serializer.save()
            library = serializer.save(owner=request.user)
            library.latitude = request.data.get('latitude')
            library.longitude = request.data.get('longitude')
            library.save()
            return Response({'message': 'Library created successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================= Update Library API ============================
class UpdateLibraryAPI(APIView):
    permission_classes = [IsAdminUser]
    
    def put(self, request, library_id):
        library = get_object_or_404(Library, id=library_id)
        serializer = LibrarySerializer(library, data=request.data, partial=True)
        
        if serializer.is_valid():
            updated_library = serializer.save()
            # Update latitude and longitude if provided
            updated_library.latitude = request.data.get('latitude', updated_library.latitude)
            updated_library.longitude = request.data.get('longitude', updated_library.longitude)
            updated_library.save()
            return Response({'message': 'Library updated successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# ========================= Update Student Profile API ============================
class UpdateStudentProfileAPI(APIView):
    def put(self, request, user_id):
        user_profile = get_object_or_404(UserProfile, user__id=user_id)
        serializer = UserProfileSerializer(user_profile, data=request.data, partial=True)

        if serializer.is_valid():
            updated_profile = serializer.save()
            # Update latitude and longitude if provided
            updated_profile.latitude = request.data.get('latitude', updated_profile.latitude)
            updated_profile.longitude = request.data.get('longitude', updated_profile.longitude)
            updated_profile.save()
            return Response({'message': 'Profile updated successfully'}, status=status.HTTP_200_OK)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# UserProfileAPI to create and retrieve user profiles
class UserProfileAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        profiles = UserProfile.objects.all()
        serializer = UserProfileSerializer(profiles, many=True)
        return Response(serializer.data)

    def post(self, request, *args, **kwargs):
        serializer = UserProfileSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# ========================= Approve Users API ============================
class ApproveUserAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        # Check if the user is a superadmin or admin
        if not (request.user.is_superuser or request.user.is_staff):
            return Response({'error': 'You do not have permission to approve users.'}, status=status.HTTP_403_FORBIDDEN)

        user_profile = get_object_or_404(UserProfile, id=user_id)
        user_profile.approved = True
        user_profile.save()
        return Response({'status': 'User approved'}, status=status.HTTP_200_OK)



# ========================= Assign Role API ============================
class AssignRoleAPI(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, user_id, *args, **kwargs):
        # Check if the requesting user has a UserProfile, and ensure they're a superadmin
        try:
            user_profile_requesting = request.user.userprofile
        except UserProfile.DoesNotExist:
            return Response({'error': 'User profile not found for the requesting user.'}, status=status.HTTP_404_NOT_FOUND)

        if user_profile_requesting.role != 'superadmin':
            return Response({'error': 'You do not have permission to assign roles.'}, status=status.HTTP_403_FORBIDDEN)

        # Get the user profile to whom the role will be assigned
        user_profile = get_object_or_404(UserProfile, id=user_id)

        # Get the role and optional library ID from the request data
        role = request.data.get('role')
        library_id = request.data.get('library_id')  # Optional for both admin and student

        if not role or role not in ['superadmin', 'admin', 'student']:
            return Response({'error': 'Invalid or missing role.'}, status=status.HTTP_400_BAD_REQUEST)

        # If library_id is provided, assign it to the user profile (for both admin and student)
        if library_id:
            library = get_object_or_404(Library, id=library_id)
            user_profile.library = library

        # Assign the new role
        user_profile.role = role

        # Save the updated user profile
        user_profile.save()

        return Response({'status': f'Role {role} assigned to user {user_profile.user.username}'}, status=status.HTTP_200_OK)



# RetrieveLibraryAPI to get a single library by its ID
class RetrieveLibraryAPI(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Library.objects.all()
    serializer_class = LibrarySerializer

    def get(self, request, *args, **kwargs):
        library = get_object_or_404(Library, id=kwargs.get('library_id'))
        serializer = LibrarySerializer(library)
        return Response(serializer.data, status=status.HTTP_200_OK)


# DeleteLibraryAPI to delete a library by its ID
class DeleteLibraryAPI(DestroyAPIView):
    permission_classes = [IsAuthenticated]
    queryset = Library.objects.all()

    def delete(self, request, *args, **kwargs):
        library = get_object_or_404(Library, id=kwargs.get('library_id'))
        library.delete()
        return Response({'status': 'Library deleted'}, status=status.HTTP_204_NO_CONTENT)

















































# ========================= Assign Role API ============================
# class AssignRoleAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id, *args, **kwargs):
#         # Only superadmin can assign roles
#         if not request.user.userprofile.role == 'superadmin':
#             return Response({'error': 'You do not have permission to assign roles.'}, status=status.HTTP_403_FORBIDDEN)

#         # Get the user profile to whom the role will be assigned
#         user_profile = get_object_or_404(UserProfile, id=user_id)

#         # Get the role and optional library ID from the request data
#         role = request.data.get('role')
#         library_id = request.data.get('library_id')  # Required only if role is 'admin'

#         if not role or role not in ['superadmin', 'admin', 'student']:
#             return Response({'error': 'Invalid or missing role.'}, status=status.HTTP_400_BAD_REQUEST)

#         # If assigning 'admin', ensure library_id is provided
#         if role == 'admin':
#             if not library_id:
#                 return Response({'error': 'Library ID must be provided for admin role.'}, status=status.HTTP_400_BAD_REQUEST)
#             library = get_object_or_404(Library, id=library_id)
#             user_profile.library = library

#         # Assign the new role
#         user_profile.role = role

#         # Save the updated user profile
#         user_profile.save()

#         return Response({'status': f'Role {role} assigned to user {user_profile.user.username}'}, status=status.HTTP_200_OK)





# ========================= Student Signup API ============================
# class StudentSignupAPI(APIView):
#     def post(self, request):
#         serializer = StudentSignupSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             # Create user profile
#             UserProfile.objects.create(user=user, role='student')
#             return Response({'message': 'Student registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)






# ========================= Library List API with Geo-location ============================
# class LibraryListAPI(APIView):
#     # Removed authentication requirement to allow public access
#     def get(self, request):
#         user_lat = request.query_params.get('lat')  # User's latitude
#         user_lng = request.query_params.get('lng')  # User's longitude

#         # Fetch all libraries
#         libraries = Library.objects.all()
#         library_data = []

#         if user_lat and user_lng:
#             user_location = (float(user_lat), float(user_lng))
#             for library in libraries:
#                 library_location = (library.latitude, library.longitude)
#                 distance = calculate_distance(user_location, library_location)
#                 library_data.append({
#                     'name': library.name,
#                     'address': library.address,
#                     'distance': f"{distance:.2f} km",
#                     'owner': library.owner.username,
#                     'seat_availability': library.seats.count()
#                 })
#         else:
#             # If no user location is provided, return all libraries without distance calculation
#             for library in libraries:
#                 library_data.append({
#                     'name': library.name,
#                     'address': library.address,
#                     'owner': library.owner.username,
#                     'seat_availability': library.seats.count()
#                 })
            

#         return Response(library_data)






# ========================= Create Library API with Geo-location ============================
# class CreateLibraryAPI(APIView):
#     permission_classes = [IsAdminUser]

#     def post(self, request):
#         serializer = LibrarySerializer(data=request.data)
#         if serializer.is_valid():
#             # Assign the current user as the owner
#             library = serializer.save(owner=request.user)
#             return Response({'message': 'Library created successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)




# ApproveUserAPI for admins to approve user registration
# class ApproveUserAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id, *args, **kwargs):
#         try:
#             user_profile = get_object_or_404(UserProfile, id=user_id)
#             user_profile.approved = True
#             user_profile.save()
#             return Response({'status': 'User approved'}, status=status.HTTP_200_OK)
#         except UserProfile.DoesNotExist:
#             return Response({'error': 'User not found'}, status=status.HTTP_404_NOT_FOUND)



# ApproveUserAPI for admins to approve user registration
# class ApproveUserAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id, *args, **kwargs):
#         # Check if the user is a superadmin or admin
#         if not (request.user.is_superuser or request.user.is_staff):
#             return Response({'error': 'You do not have permission to approve users.'}, status=status.HTTP_403_FORBIDDEN)

#         user_profile = get_object_or_404(UserProfile, id=user_id)
#         user_profile.approved = True
#         user_profile.save()
#         return Response({'status': 'User approved'}, status=status.HTTP_200_OK)




# class ApproveUserAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id, *args, **kwargs):
#         # Check if the user making the request is a superadmin
#         if not request.user.is_superadmin:  # Adjust this check according to your user model
#             return Response({'error': 'Permission denied. Only superadmin can approve users.'},
#                             status=status.HTTP_403_FORBIDDEN)

#         user_profile = get_object_or_404(UserProfile, id=user_id)

#         # Validate and update the role
#         serializer = ApproveUserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
        
#         user_profile.approved = True
#         user_profile.role = serializer.validated_data['role']
#         user_profile.save()

#         return Response({'status': 'User approved', 'role': user_profile.role}, status=status.HTTP_200_OK)



# class ApproveUserAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id, *args, **kwargs):
#         # Get the user profile for the requesting user
#         user_profile = get_object_or_404(UserProfile, user=request.user)

#         # Check if the user is a superadmin
#         if not user_profile.is_superadmin:
#             return Response({'error': 'Permission denied. Only superadmin can approve users.'},
#                             status=status.HTTP_403_FORBIDDEN)

#         user_profile_to_approve = get_object_or_404(UserProfile, id=user_id)

#         # Validate and update the role
#         serializer = ApproveUserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user_profile_to_approve.approved = True
#         user_profile_to_approve.role = serializer.validated_data['role']
#         user_profile_to_approve.save()

#         return Response({'status': 'User approved', 'role': user_profile_to_approve.role}, status=status.HTTP_200_OK)




# class ApproveUserAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id, *args, **kwargs):
#         print("Request received to approve user:", user_id)
#         # Check if the requesting user is a superadmin
#         requesting_user_profile = get_object_or_404(UserProfile, user=request.user)
#         if requesting_user_profile.role != 'superadmin':
#             return Response({'error': 'Permission denied. Only superadmin can approve users.'},
#                             status=status.HTTP_403_FORBIDDEN)

#         print(f"Trying to approve UserProfile with ID: {user_id}")

#         # Attempt to get the user profile to approve
#         try:
#             user_profile_to_approve = UserProfile.objects.get(id=user_id)
#             print(f"UserProfile found: {user_profile_to_approve}")
#         except UserProfile.DoesNotExist:
#             print(f"No UserProfile found with ID: {user_id}")
#             return Response({'error': 'UserProfile not found.'}, status=status.HTTP_404_NOT_FOUND)

#         # Validate and update the role
#         serializer = ApproveUserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user_profile_to_approve.approved = True
#         user_profile_to_approve.role = serializer.validated_data['role']
#         user_profile_to_approve.save()

#         return Response({'status': 'User approved', 'role': user_profile_to_approve.role}, status=status.HTTP_200_OK)

# class ApproveUserAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def post(self, request, user_id, *args, **kwargs):
#         print("Request received to approve user:", user_id)
#         # Check if the requesting user is a superadmin
#         requesting_user_profile = get_object_or_404(UserProfile, user=request.user)
#         if requesting_user_profile.role != 'superadmin':
#             return Response({'error': 'Permission denied. Only superadmin can approve users.'},
#                             status=status.HTTP_403_FORBIDDEN)

#         print(f"Trying to approve UserProfile with User ID: {user_id}")

#         # Get the UserProfile based on the User's ID
#         user_profile_to_approve = get_object_or_404(UserProfile, user__id=user_id)
#         print(f"UserProfile found: {user_profile_to_approve}")

#         # Validate and update the role
#         serializer = ApproveUserSerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         user_profile_to_approve.approved = True
#         user_profile_to_approve.role = serializer.validated_data['role']
#         user_profile_to_approve.save()

#         return Response({'status': 'User approved', 'role': user_profile_to_approve.role}, status=status.HTTP_200_OK)





# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework import status
# from rest_framework.permissions import IsAuthenticated, IsAdminUser
# from django.shortcuts import get_object_or_404
# from .models import Library, Seat, UserProfile, Payment
# from .serializers import StudentSignupSerializer, UserProfileSerializer, LibrarySerializer, SeatSerializer
# from rest_framework import generics
# from rest_framework.permissions import IsAuthenticated
# from rest_framework.authentication import TokenAuthentication
# from geopy.distance import geodesic

# def calculate_distance(user_location, library_location):
#     return geodesic(user_location, library_location).km

# # class StudentSignupAPI(APIView):
# #     def post(self, request):
# #         serializer = StudentSignupSerializer(data=request.data)
# #         if serializer.is_valid():
# #             user = serializer.save()
# #             UserProfile.objects.create(user=user, role='student')
# #             return Response({'message': 'Student registered successfully'}, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# class StudentSignupAPI(APIView):
#     def post(self, request):
#         serializer = StudentSignupSerializer(data=request.data)
#         if serializer.is_valid():
#             user = serializer.save()
#             # Automatically create user profile for student
#             UserProfile.objects.create(user=user, role='student')
#             return Response({'message': 'Student registered successfully'}, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



# # class StudentProfileAPI(APIView):
# #     permission_classes = [IsAuthenticated]

# #     def get(self, request):
# #         profile = get_object_or_404(UserProfile, user=request.user)
# #         serializer = UserProfileSerializer(profile)
# #         return Response(serializer.data)

# #     def put(self, request):
# #         profile = get_object_or_404(UserProfile, user=request.user)
# #         serializer = UserProfileSerializer(profile, data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response({'message': 'Profile updated successfully'})
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)



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


# # class LibraryListAPI(APIView):
# #     permission_classes = [IsAuthenticated]

# #     def get(self, request):
# #         # print(f"Authorization Header: {request.headers.get('Authorization')}")
# #         libraries = Library.objects.all()
# #         serializer = LibrarySerializer(libraries, many=True)
# #         permission_classes = [IsAuthenticated]
# #         return Response(serializer.data)



# class LibraryListAPI(APIView):
#     permission_classes = []  # Allow unauthenticated users to access this API

#     def get(self, request):
#         user_lat = request.query_params.get('lat')
#         user_lon = request.query_params.get('lon')

#         if not user_lat or not user_lon:
#             return Response({"error": "Please provide latitude and longitude."}, status=status.HTTP_400_BAD_REQUEST)

#         user_location = (float(user_lat), float(user_lon))
#         libraries = Library.objects.all()

#         result = []
#         for library in libraries:
#             library_location = (library.latitude, library.longitude)  # Assuming Library model has latitude & longitude
#             distance = calculate_distance(user_location, library_location)
#             result.append({
#                 "name": library.name,
#                 "address": library.address,  # Assuming you have address field
#                 "owner": library.owner.username,  # Assuming owner is a foreign key to User
#                 "distance_km": distance,
#                 "available_seats": library.seats.filter(is_booked=False).count(),
#                 "total_seats": library.seats.count()
#             })

#         return Response(result)




# class SeatAvailabilityAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, library_id):
#         library = get_object_or_404(Library, id=library_id)
#         seats = library.seats.all()
#         serializer = SeatSerializer(seats, many=True)
#         return Response({'library': library.name, 'seats': serializer.data})
    


# class ApproveStudentAPI(APIView):
#     permission_classes = [IsAdminUser]

#     def post(self, request, student_id):
#         student = get_object_or_404(UserProfile, id=student_id)
#         payment = Payment.objects.filter(student=student.user, is_confirmed=True).first()
#         if payment:
#             student.approved = True
#             student.save()
#             return Response({'message': 'Student approved successfully'})
#         else:
#             return Response({'error': 'Payment not confirmed'}, status=status.HTTP_400_BAD_REQUEST)
        




# # ======================================================================================

# # class CreateLibraryAPI(APIView):
# #     permission_classes = [IsAdminUser]

# #     def post(self, request):
# #         serializer = LibrarySerializer(data=request.data)
# #         if serializer.is_valid():
# #             serializer.save()
# #             return Response(serializer.data, status=status.HTTP_201_CREATED)
# #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class CreateLibraryAPI(APIView):
#     permission_classes = [IsAdminUser]

#     def post(self, request):
#         data = request.data
#         latitude = data.get('latitude')
#         longitude = data.get('longitude')

#         if not latitude or not longitude:
#             return Response({'error': 'Latitude and longitude are required'}, status=status.HTTP_400_BAD_REQUEST)

#         serializer = LibrarySerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_201_CREATED)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class RetrieveLibraryAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request, library_id):
#         library = get_object_or_404(Library, id=library_id)
#         serializer = LibrarySerializer(library)
#         return Response(serializer.data, status=status.HTTP_200_OK)


# class UpdateLibraryAPI(APIView):
#     permission_classes = [IsAdminUser]

#     def put(self, request, library_id):
#         library = get_object_or_404(Library, id=library_id)
#         serializer = LibrarySerializer(library, data=request.data, partial=True)
#         if serializer.is_valid():
#             serializer.save()
#             return Response(serializer.data, status=status.HTTP_200_OK)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


# class DeleteLibraryAPI(APIView):
#     permission_classes = [IsAdminUser]

#     def delete(self, request, library_id):
#         library = get_object_or_404(Library, id=library_id)
#         library.delete()
#         return Response({'message': 'Library deleted successfully'}, status=status.HTTP_204_NO_CONTENT)


# class ListLibrariesAPI(APIView):
#     permission_classes = [IsAuthenticated]

#     def get(self, request):
#         libraries = Library.objects.all()
#         serializer = LibrarySerializer(libraries, many=True)
#         return Response(serializer.data, status=status.HTTP_200_OK)

