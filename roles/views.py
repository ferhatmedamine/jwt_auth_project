from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render
from django.core.exceptions import PermissionDenied

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