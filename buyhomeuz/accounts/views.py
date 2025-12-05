from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib.auth.decorators import login_required, permission_required
from django.core.exceptions import PermissionDenied
from django.contrib.auth.models import User, Group
from django.db import IntegrityError
from appointments.models import Appointment
from .forms import UserForm, UserRegisterForm, GroupForm, UserCreateForm

def register_view(request):
    if request.method == 'POST':
        form = UserRegisterForm(request.POST)
        if form.is_valid():
            try:
                user = form.save()
                user.groups.add(Group.objects.get(name='Customer'))
                login(request, user)
                messages.success(request, f'Welcome {user.username}! Your account has been created.')
                return redirect('home')
            except IntegrityError:
                messages.success(request, 'Welcome! Your account has been created.')
                return redirect('home')
    else:
        form = UserRegisterForm()
    return render(request, 'accounts/login.html', {
        'form': form,
        'form_type': 'register'
    })

def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'Welcome back, {username}!')
                next_url = request.GET.get('next') or request.POST.get('next', 'home')
                return redirect(next_url)
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {
        'form': form,
        'form_type': 'login'
    })
    
def logout_view(request):
    logout(request)
    messages.info(request, 'You have been logged out successfully.')
    return redirect('home')

@login_required
def dashboard_view(request):
    has_access = (
        request.user.has_perm('auth.view_user') or
        request.user.has_perm('auth.view_group') or
        request.user.has_perm('properties.view_property')
    )
    if not has_access:
        raise PermissionDenied("You do not have permission to access the dashboard.")
    return render(request, 'accounts/dashboard.html')

@login_required
def profile_view(request):
    user_appointments = Appointment.objects.filter(
        customer=request.user
    ).select_related('property', 'manager').order_by('-created_at')

    manager_appointments = Appointment.objects.filter(
        manager=request.user
    ).select_related('property', 'customer').order_by('-created_at')
    
    pending_appointments = None
    if request.user.has_perm('appointments.change_appointment'):
        pending_appointments = Appointment.objects.filter(
            status='pending'
        ).select_related('property', 'customer').order_by('created_at')
    
    return render(request, 'accounts/profile.html', {
        'user': request.user,
        'user_appointments': user_appointments,
        'pending_appointments': pending_appointments,
        'manager_appointments': manager_appointments,
    })

@permission_required('auth.view_user', raise_exception=True)
def users_list(request):
    users = User.objects.all().prefetch_related('groups').filter(is_staff=False)
    return render(request, 'accounts/users_list.html', {'users': users})

@permission_required('auth.add_user', raise_exception=True)
def user_create(request):
    if request.method == 'POST':
        form = UserCreateForm(request.POST)
        if form.is_valid():
            user = form.save()
            messages.success(request, f'User "{user.username}" created.')
            return redirect('accounts:users_list')
    else:
        form = UserCreateForm()
    return render(request, 'accounts/user_form.html', {'form': form})

@permission_required('auth.change_user', raise_exception=True)
def user_edit(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_staff:
        messages.error(request, 'You cannot edit a staff user.')
        return redirect('accounts:users_list')
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            messages.success(request, f'User "{user.username}" updated.')
            return redirect('accounts:users_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'accounts/user_form.html', {'form': form})

@permission_required('auth.delete_user', raise_exception=True)
def user_delete(request, pk):
    user = User.objects.get(pk=pk)
    if user.is_staff:
        messages.error(request, 'You cannot delete a staff user.')
        return redirect('accounts:users_list')
    user.delete()
    messages.success(request, f'User "{user.username}" deleted.')
    return redirect('accounts:users_list')

# @permission_required('auth.view_group', raise_exception=True)
# def groups_list(request):
#     groups = Group.objects.all()
#     return render(request, 'accounts/groups_list.html', {'groups': groups})

# @permission_required('auth.add_group', raise_exception=True)
# def group_create(request):
#     if request.method == 'POST':
#         form = GroupForm(request.POST)
#         if form.is_valid():
#             group = form.save()
#             messages.success(request, f'Group "{group.name}" created.')
#             return redirect('accounts:groups_list')
#     else:
#         form = GroupForm()
#     return render(request, 'accounts/group_form.html', {'form': form})

# @permission_required('auth.change_group', raise_exception=True)
# def group_edit(request, pk):
#     group = Group.objects.get(pk=pk)
#     if request.method == 'POST':
#         form = GroupForm(request.POST, instance=group)
#         if form.is_valid():
#             form.save()
#             messages.success(request, f'Group "{group.name}" updated.')
#             return redirect('accounts:groups_list')
#     else:
#         form = GroupForm(instance=group)
#     return render(request, 'accounts/group_form.html', {'form': form})

# @permission_required('auth.delete_group', raise_exception=True)
# def group_delete(request, pk):
#     group = Group.objects.get(pk=pk)
#     group.delete()
#     messages.success(request, f'Group "{group.name}" deleted.')
#     return redirect('accounts:groups_list')
