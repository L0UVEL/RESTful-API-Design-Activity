from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from .models import Announcement, User

def custom_login(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        # We need a custom auth backend to auth by email, or force them to use username.
        # For simplicity, lookup user by email to get username
        try:
            user_obj = User.objects.get(email=email)
            username = user_obj.username
        except User.DoesNotExist:
            username = None
            
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            # Route based on staff status
            if user.is_staff:
                return redirect('admin-dashboard')
            else:
                return redirect('student-dashboard') # Placeholder 
        else:
            messages.error(request, 'Invalid email or password.')
            
    return render(request, 'auth/login.html')

def admin_dashboard(request):
    # Fetch initial data to pass to template
    announcements = Announcement.objects.all().order_by('-timestamp')
    students = User.objects.filter(role__name__icontains='student') # Adjust as needed based on schema
    if not students.exists():
        # Fallback if roles aren't strictly populated yet
        students = User.objects.exclude(is_staff=True)
        
    context = {
        'announcements': announcements,
        'students': students,
    }
    return render(request, 'admin/admin_dashboard.html', context)

def admin_user_management(request):
    return render(request, 'admin/admin_user_management.html')

def custom_logout(request):
    from django.contrib.auth import logout
    logout(request)
    return redirect('custom-login')

def admin_appointments(request):
    from .models import Appointment
    appointments = Appointment.objects.all().order_by('-appointment_date')
    return render(request, 'admin/admin_appointments.html', {'appointments': appointments})

def student_dashboard(request):
    from .models import Announcement
    announcements = Announcement.objects.all().order_by('-timestamp')
    return render(request, 'student/student_dashboard.html', {'announcements': announcements})
