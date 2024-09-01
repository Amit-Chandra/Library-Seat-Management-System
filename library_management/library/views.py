from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from .models import Library, Seat, UserProfile, Payment
from .forms import StudentSignupForm, UserProfileForm

def student_signup(request):
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user, role='student')
            return redirect('login')  # Redirect to login page
    else:
        form = StudentSignupForm()
    return render(request, 'library/student_signup.html', {'form': form})

@login_required
def student_profile(request):
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            return redirect('library_list')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'library/student_profile.html', {'form': form})

@login_required
def library_list(request):
    libraries = Library.objects.all()
    return render(request, 'library/library_list.html', {'libraries': libraries})

@login_required
def seat_availability(request, library_id):
    library = Library.objects.get(id=library_id)
    seats = library.seats.all()
    return render(request, 'library/seat_availability.html', {'library': library, 'seats': seats})

@login_required
def approve_student(request, student_id):
    student = UserProfile.objects.get(id=student_id)
    if request.method == 'POST' and request.user.userprofile.role == 'admin':
        payment = Payment.objects.get(student=student.user, is_confirmed=True)
        if payment:
            student.approved = True
            student.save()
            return redirect('library_list')
    return render(request, 'library/approve_student.html', {'student': student})
































# from django.shortcuts import render, redirect
# from django.http import HttpResponse

# def student_signup(request):
#     # Your logic here
#     return render(request, 'student_signup.html')

# def library_list(request):
#     # Your logic here
#     libraries = []  # Replace with actual query
#     return render(request, 'library_list.html', {'libraries': libraries})

# def seat_availability(request):
#     # Your logic here
#     seats = []  # Replace with actual query
#     library = {}  # Replace with actual library
#     return render(request, 'seat_availability.html', {'seats': seats, 'library': library})

# def student_profile(request):
#     # Your logic here
#     return render(request, 'student_profile.html')

# def approve_student(request):
#     # Your logic here
#     pending_students = []  # Replace with actual query
#     return render(request, 'approve_student.html', {'pending_students': pending_students})
