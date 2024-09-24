from django.urls import path
from django.contrib import admin
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .api_views import (
    ApproveUserAPI,
    SignupAPI,
    LoginAPI,
    LibraryListAPI,
    SeatAvailabilityAPI,
    UserProfileAPI,
    CreateLibraryAPI,
    RetrieveLibraryAPI,
    UpdateLibraryAPI,
    DeleteLibraryAPI,
    AssignRoleAPI
)

urlpatterns = [
    path('admin/', admin.site.urls),
    
    # JWT Authentication
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Student Signup
    path('user-signup/', SignupAPI.as_view(), name='user-signup'),
    path('user-login/', LoginAPI.as_view(), name='user-login'),

    path('user-profiles/', UserProfileAPI.as_view(), name='user-profile-list'),  # List and create user profiles
    path('user-profiles/approve/<int:user_id>/', ApproveUserAPI.as_view(), name='approve-user'), 
    path('assign-role/<int:user_id>/', AssignRoleAPI.as_view(), name='assign_role'),
    

    # Library List (Public Access)
    path('library-list/', LibraryListAPI.as_view(), name='library-list'),

    # Seat Availability
    path('seat-availability/<int:library_id>/', SeatAvailabilityAPI.as_view(), name='seat-availability'),

    path('library/<int:library_id>/', RetrieveLibraryAPI.as_view(), name='retrieve-library'),  # Retrieve a single library

    # Library CRUD Operations (Admin Only)
    path('create-library/', CreateLibraryAPI.as_view(), name='create-library'),
    path('update-library/<int:library_id>/', UpdateLibraryAPI.as_view(), name='update-library'),
    path('delete-library/<int:library_id>/', DeleteLibraryAPI.as_view(), name='delete-library'),
]





# from django.urls import path
# from .api_views import (
#     StudentSignupAPI,
#     LibraryListAPI,
#     SeatAvailabilityAPI,
#     CreateLibraryAPI,
#     UpdateLibraryAPI,
#     UpdateStudentProfileAPI
# )

# urlpatterns = [
#     # Student Signup API
#     path('student-signup/', StudentSignupAPI.as_view(), name='student-signup'),

#     # Library List API with optional geo-location filtering
#     path('library-list/', LibraryListAPI.as_view(), name='library-list'),

#     # Seat Availability API for a specific library
#     path('seat-availability/<int:library_id>/', SeatAvailabilityAPI.as_view(), name='seat-availability'),

#     # Create Library API (Admin only)
#     path('create-library/', CreateLibraryAPI.as_view(), name='create-library'),

#     # Update Library API (Admin only)
#     path('update-library/<int:library_id>/', UpdateLibraryAPI.as_view(), name='update-library'),

#     # Update Student Profile API
#     path('update-student-profile/<int:user_id>/', UpdateStudentProfileAPI.as_view(), name='update-student-profile'),
# ]






















# from django.urls import path
# from django.contrib.auth import views as auth_views
# from django.contrib import admin
# from .api_views import CreateLibraryAPI, DeleteLibraryAPI, ListLibrariesAPI, StudentSignupAPI, StudentProfileAPI, LibraryListAPI, SeatAvailabilityAPI, ApproveStudentAPI, RetrieveLibraryAPI, UpdateLibraryAPI
# from .regular_views import student_signup, student_profile, library_list, seat_availability, approve_student
# from . import regular_views
# from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
# # from rest_framework_simplejwt.views import (
# #     TokenObtainPairView,
# #     TokenRefreshView,
# # )


# urlpatterns = [
#     path('admin/', admin.site.urls),
#     # path('login/', views.login_view, name='login'),
#     # API Endpoints
#     # path('api/signup/', StudentSignupAPI.as_view(), name='student_signup_api'),
#     # path('api/profile/', StudentProfileAPI.as_view(), name='student_profile_api'),
#     # path('api/libraries/', LibraryListAPI.as_view(), name='library_list_api'),
#     # path('library/<int:library_id>/', RetrieveLibraryAPI.as_view(), name='retrieve_library'),
#     # path('api/libraries/<int:library_id>/seats/', SeatAvailabilityAPI.as_view(), name='seat_availability_api'),
#     # path('api/approve_student/<int:student_id>/', ApproveStudentAPI.as_view(), name='approve_student_api'),
#     # path('api/admin/libraries/create/', CreateLibraryAPI.as_view(), name='create-library'),
#     path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
#     path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),


#     path('studentsignup/', StudentSignupAPI.as_view(), name='student_signup_api'),
#     path('signup/', student_signup, name='student_signup_api'),

#     # Student Profile
#     # path('profile/', StudentProfileAPI.as_view(), name='student_profile'),
#     path('profileview/', StudentProfileAPI.as_view(), name='student_profile_api'),
#     path('profile/', student_profile, name='student_profile'),

#     # Library List
#     path('librarieslist/', LibraryListAPI.as_view(), name='library_list_api'),
#     path('libraries/', library_list, name='library_list'),

#     # Seat Availability for a specific library
#     path('librarieslist/<int:library_id>/seats/', SeatAvailabilityAPI.as_view(), name='seat_availability_api'),
#     path('libraries/<int:library_id>/seats/', seat_availability, name='seat_availability'),

#     # Approve a student
#     path('studentsapproval/<int:student_id>/approve/', ApproveStudentAPI.as_view(), name='approve_student_api'),
#     path('students/<int:student_id>/approve/', approve_student, name='approve_student'),

#     # Create a new library
#     path('libraries/create/', CreateLibraryAPI.as_view(), name='create_library'),

#     # Retrieve a specific library
#     path('libraries/<int:library_id>/', RetrieveLibraryAPI.as_view(), name='retrieve_library'),

#     # Update a specific library
#     path('libraries/update/<int:library_id>/', UpdateLibraryAPI.as_view(), name='update_library'),

#     # Delete a specific libraryc
#     path('libraries/delete/<int:library_id>/', DeleteLibraryAPI.as_view(), name='delete_library'),

#     # List all libraries (This seems redundant with LibraryListAPI, so you may want to choose one or the other)
#     path('libraries/all/', ListLibrariesAPI.as_view(), name='list_libraries'),


#     # Regular Views
#     path('', regular_views.home, name='home'),  # Home view
#     path('signup/', regular_views.student_signup, name='student_signup'),  # Student signup
#     path('profile/', regular_views.student_profile, name='student_profile'),  # Student profile
#     path('libraries/', regular_views.library_list, name='library_list'),  # List libraries
#     path('libraries/<int:library_id>/seats/', regular_views.seat_availability, name='seat_availability'),  # Seat availability
#     path('approve_student/<int:student_id>/', regular_views.approve_student, name='approve_student'),  # Approve student
#     path('admin_panel/', regular_views.admin_panel, name='admin_panel'),  # Admin panel for superusers
#     path('admin/create/', regular_views.create_admin, name='create_admin'),  # Create admin
#     path('admin/update/<int:admin_id>/', regular_views.update_admin, name='update_admin'),  # Update admin
#     path('admin/delete/<int:admin_id>/', regular_views.delete_admin, name='delete_admin'),  # Delete admin
#     path('accounts/logout/', auth_views.LogoutView.as_view(), name='logout'),

# ]
