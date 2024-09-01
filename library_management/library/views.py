from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from .models import Library, Seat, UserProfile, Payment
from .serializers import StudentSignupSerializer, UserProfileSerializer, LibrarySerializer, SeatSerializer


class StudentSignupAPI(APIView):
    def post(self, request):
        serializer = StudentSignupSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            UserProfile.objects.create(user=user, role='student')
            return Response({'message': 'Student registered successfully'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


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


class LibraryListAPI(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        libraries = Library.objects.all()
        serializer = LibrarySerializer(libraries, many=True)
        return Response(serializer.data)


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



















# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from django.contrib.auth.models import User
# from .models import Library, Seat, UserProfile, Payment
# from .forms import StudentSignupForm, UserProfileForm

# def student_signup(request):
#     if request.method == 'POST':
#         form = StudentSignupForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.set_password(form.cleaned_data['password'])
#             user.save()
#             UserProfile.objects.create(user=user, role='student')
#             return redirect('login')  # Redirect to login page
#     else:
#         form = StudentSignupForm()
#     return render(request, 'library/student_signup.html', {'form': form})

# @login_required
# def student_profile(request):
#     profile = UserProfile.objects.get(user=request.user)
#     if request.method == 'POST':
#         form = UserProfileForm(request.POST, instance=profile)
#         if form.is_valid():
#             form.save()
#             return redirect('library_list')
#     else:
#         form = UserProfileForm(instance=profile)
#     return render(request, 'library/student_profile.html', {'form': form})

# @login_required
# def library_list(request):
#     libraries = Library.objects.all()
#     return render(request, 'library/library_list.html', {'libraries': libraries})

# @login_required
# def seat_availability(request, library_id):
#     library = Library.objects.get(id=library_id)
#     seats = library.seats.all()
#     return render(request, 'library/seat_availability.html', {'library': library, 'seats': seats})

# @login_required
# def approve_student(request, student_id):
#     student = UserProfile.objects.get(id=student_id)
#     if request.method == 'POST' and request.user.userprofile.role == 'admin':
#         payment = Payment.objects.get(student=student.user, is_confirmed=True)
#         if payment:
#             student.approved = True
#             student.save()
#             return redirect('library_list')
#     return render(request, 'library/approve_student.html', {'student': student})



























