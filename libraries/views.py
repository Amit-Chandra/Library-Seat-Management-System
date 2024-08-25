from django.contrib.auth.decorators import login_required
from django.http import HttpResponseForbidden
from django.shortcuts import render, get_object_or_404, redirect
from .forms import LibraryForm
from .models import Library, Seat

@login_required
def library_create(request):
    # Only super admins can create libraries
    if request.user.role != 'super_admin':
        return HttpResponseForbidden("You do not have permission to create a library.")

    if request.method == 'POST':
        form = LibraryForm(request.POST)
        if form.is_valid():
            library = form.save(commit=False)
            library.admin = request.user  # Set the super admin as the library admin
            library.save()
            return redirect('library_list')
    else:
        form = LibraryForm()
    return render(request, 'libraries/library_form.html', {'form': form})


@login_required
def library_list(request):
    if request.user.role == 'super_admin':
        libraries = Library.objects.all()  # Super admins can see all libraries
    elif request.user.role == 'admin':
        libraries = Library.objects.filter(admin=request.user)  # Admins can see only their library
    else:
        return HttpResponseForbidden("You do not have permission to view libraries.")
    
    return render(request, 'libraries/library_list.html', {'libraries': libraries})


@login_required
def library_detail(request, library_id):
    library = get_object_or_404(Library, id=library_id)
    
    if request.user.role == 'super_admin':
        # Super admins can access any library
        pass
    elif request.user.role == 'admin' and library.admin != request.user:
        # Admins can only access their own library
        return HttpResponseForbidden("You do not have permission to view this library.")
    
    # Fetch related seats for the library
    seats = Seat.objects.filter(library=library)
    
    return render(request, 'libraries/library_detail.html', {
        'library': library,
        'seats': seats,
    })
