from django.shortcuts import get_object_or_404
from django.http import JsonResponse
from django.contrib.auth.models import User
from organisation.models import Organisation
from .models import UserRole

def add_user_to_organisation(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        organisation_id = request.POST.get('organisation_id')
        role = request.POST.get('role', 'student')

        user = get_object_or_404(User, id=user_id)
        organisation = get_object_or_404(Organisation, id=organisation_id)

        user_role = UserRole.objects.add_user_to_organisation(user, organisation, role)
        return JsonResponse({'status': 'success', 'user_role_id': user_role.id})

def update_user_role(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        organisation_id = request.POST.get('organisation_id')
        new_role = request.POST.get('new_role')

        user = get_object_or_404(User, id=user_id)
        organisation = get_object_or_404(Organisation, id=organisation_id)

        user_role = UserRole.objects.update_user_role(user, organisation, new_role)
        return JsonResponse({'status': 'success', 'user_role_id': user_role.id})

def remove_user_from_organisation(request):
    if request.method == 'POST':
        user_id = request.POST.get('user_id')
        organisation_id = request.POST.get('organisation_id')

        user = get_object_or_404(User, id=user_id)
        organisation = get_object_or_404(Organisation, id=organisation_id)

        UserRole.objects.remove_user_from_organisation(user, organisation)
        return JsonResponse({'status': 'success'})