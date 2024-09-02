from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Library, Seat, UserProfile, Payment
from .forms import StudentSignupForm, UserProfileForm
from django.shortcuts import LibraryForm

def home(request):
    return render(request, 'library/home.html')

def student_signup(request):
    """View for student registration."""
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.save()
            UserProfile.objects.create(user=user, role='student')
            messages.success(request, 'Student registered successfully. Please log in.')
            return redirect('login')  # Redirect to login page
    else:
        form = StudentSignupForm()
    return render(request, 'library/student_signup.html', {'form': form})

@login_required
def student_profile(request):
    """View for student profile management."""
    profile = UserProfile.objects.get(user=request.user)
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=profile)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully.')
            return redirect('library_list')
    else:
        form = UserProfileForm(instance=profile)
    return render(request, 'library/student_profile.html', {'form': form})

@login_required
def library_list(request):
    """View for listing all libraries."""
    libraries = Library.objects.all()
    return render(request, 'library/library_list.html', {'libraries': libraries})

@login_required
def seat_availability(request, library_id):
    """View to check seat availability in a library."""
    library = get_object_or_404(Library, id=library_id)
    seats = library.seats.all()
    return render(request, 'library/seat_availability.html', {'library': library, 'seats': seats})

@login_required
def approve_student(request, student_id):
    """View for approving students by an admin."""
    student = get_object_or_404(UserProfile, id=student_id)
    if request.method == 'POST' and request.user.userprofile.role == 'admin':
        payment = Payment.objects.get(student=student.user, is_confirmed=True)
        if payment:
            student.approved = True
            student.save()
            messages.success(request, 'Student approved successfully.')
            return redirect('library_list')
    return render(request, 'library/approve_student.html', {'student': student})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_panel(request):
    """View to list all admins for superuser."""
    admins = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, 'library/admin_panel.html', {'admins': admins})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_admin(request):
    """View to create a new admin by superuser."""
    if request.method == 'POST':
        form = StudentSignupForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.set_password(form.cleaned_data['password'])
            user.is_staff = True
            user.save()
            messages.success(request, 'Admin created successfully.')
            return redirect('admin_panel')
    else:
        form = StudentSignupForm()
    return render(request, 'library/create_admin.html', {'form': form})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_admin(request, admin_id):
    """View to update an existing admin by superuser."""
    admin = get_object_or_404(User, id=admin_id, is_staff=True, is_superuser=False)
    if request.method == 'POST':
        form = StudentSignupForm(request.POST, instance=admin)
        if form.is_valid():
            admin = form.save(commit=False)
            admin.set_password(form.cleaned_data['password'])
            admin.save()
            messages.success(request, 'Admin updated successfully.')
            return redirect('admin_panel')
    else:
        form = StudentSignupForm(instance=admin)
    return render(request, 'library/update_admin.html', {'form': form, 'admin': admin})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_admin(request, admin_id):
    """View to delete an admin by superuser."""
    admin = get_object_or_404(User, id=admin_id, is_staff=True, is_superuser=False)
    if request.method == 'POST':
        admin.delete()
        messages.success(request, 'Admin deleted successfully.')
        return redirect('admin_panel')
    return render(request, 'library/delete_admin.html', {'admin': admin})



# Superuser Library Management Views
@login_required
@user_passes_test(lambda u: u.is_superuser)
def admin_panel(request):
    admins = User.objects.filter(is_staff=True, is_superuser=False)
    return render(request, 'library/admin_panel.html', {'admins': admins})

# Create Library view for Superuser
@login_required
@user_passes_test(lambda u: u.is_superuser)
def create_library(request):
    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Library created successfully.')
            return redirect('library_list')
    else:
        form = LibraryForm()
    return render(request, 'library/create_library.html', {'form': form})

# Update Library view for Superuser
@login_required
@user_passes_test(lambda u: u.is_superuser)
def update_library(request, library_id):
    library = get_object_or_404(Library, id=library_id)
    if request.method == 'POST':
        form = LibraryForm(request.POST, instance=library)
        if form.is_valid():
            form.save()
            messages.success(request, 'Library updated successfully.')
            return redirect('library_list')
    else:
        form = LibraryForm(instance=library)
    return render(request, 'library/update_library.html', {'form': form, 'library': library})

# Delete Library view for Superuser
@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_library(request, library_id):
    library = get_object_or_404(Library, id=library_id)
    if request.method == 'POST':
        library.delete()
        messages.success(request, 'Library deleted successfully.')
        return redirect('library_list')
    return render(request, 'library/delete_library.html', {'library': library})


















# from django.shortcuts import render, redirect
# from django.contrib.auth.decorators import login_required
# from .models import Library, Seat, UserProfile, Payment
# from .forms import StudentSignupForm, UserProfileForm
# from django.shortcuts import render

# def home(request):
#     return render(request, 'library/home.html')

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
