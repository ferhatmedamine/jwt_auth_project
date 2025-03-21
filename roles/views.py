from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Profile, Organisation
from .forms import UserRegisterForm, UserUpdateForm, ProfileUpdateForm

# Helper functions to check user roles
def is_org_admin(user):
    # Check if the user has a profile and is an org_admin
    if hasattr(user, 'profile'):
        return user.profile.role == 'org_admin'
    return False

def is_org_staff(user):
    # Check if the user has a profile and is an org_staff
    if hasattr(user, 'profile'):
        return user.profile.role == 'org_staff'
    return False

def is_org_user(user):
    # Check if the user has a profile and is an org_user
    if hasattr(user, 'profile'):
        return user.profile.role == 'org_user'
    return False

# Admin Dashboard View
@login_required
@user_passes_test(is_org_admin)
def admin_dashboard(request):
    """
    View for organization admins.
    Only users with the 'org_admin' role can access this view.
    """
    return render(request, 'roles/org_admin/admin_dashboard.html')

# Staff Dashboard View
@login_required
@user_passes_test(is_org_staff)
def staff_dashboard(request):
    """
    View for organization staff.
    Only users with the 'org_staff' role can access this view.
    """
    return render(request, 'roles/org_staff/staff_dashboard.html')

# User Dashboard View
@login_required
@user_passes_test(is_org_user)
def user_dashboard(request):
    """
    View for organization users.
    Only users with the 'org_user' role can access this view.
    """
    return render(request, 'roles/org_user/user_dashboard.html')

# Example of a view that raises a 403 error for unauthorized access
@login_required
def restricted_view(request):
    """
    Example view that raises a 403 error if the user is not an admin.
    """
    if not is_org_admin(request.user):
        raise PermissionDenied("You do not have permission to access this page.")
    return render(request, 'roles/org_admin/restricted_page.html')

# CRUD Operations for Users

# Create User
def register(request):
    """
    View for registering a new user.
    """
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            # Create a profile for the new user
            Profile.objects.create(user=user)
            return redirect('login')
    else:
        form = UserRegisterForm()
    return render(request, 'register.html', {'form': form})

# Read User (Profile)
@login_required
def profile(request):
    """
    View for displaying the current user's profile.
    """
    return render(request, 'profile.html')

# Update User
@login_required
def update_profile(request):
    """
    View for updating the current user's profile.
    """
    if request.method == 'POST':
        user_form = UserUpdateForm(request.POST, instance=request.user)
        profile_form = ProfileUpdateForm(request.POST, instance=request.user.profile)
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return redirect('profile')
    else:
        user_form = UserUpdateForm(instance=request.user)
        profile_form = ProfileUpdateForm(instance=request.user.profile)
    return render(request, 'update_profile.html', {
        'user_form': user_form,
        'profile_form': profile_form,
    })

# Delete User
@login_required
@user_passes_test(is_org_admin)  # Only org_admin can delete users
def delete_user(request, user_id):
    """
    View for deleting a user.
    Only users with the 'org_admin' role can access this view.
    """
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        user.delete()
        return redirect('admin_dashboard')
    return render(request, 'confirm_delete.html', {'user': user})