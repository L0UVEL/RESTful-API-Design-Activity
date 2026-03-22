from django.db import models
from django.contrib.auth.models import AbstractUser

class Role(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class User(AbstractUser):
    # AbstractUser provides first_name, last_name, email, password, etc.
    student_id = models.CharField(max_length=50, blank=True, null=True)
    role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, blank=True)
    program = models.CharField(max_length=100, blank=True, null=True)
    requires_password_change = models.BooleanField(default=False)

    def __str__(self):
        return self.username or self.email

class HealthProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='health_profile')
    health_information = models.TextField(blank=True, null=True)
    blood_type = models.CharField(max_length=10, blank=True, null=True)
    emergency_contact = models.CharField(max_length=100, blank=True, null=True)
    last_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Health Profile"

class HealthUpdate(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='health_updates')
    checkin_date = models.DateTimeField(auto_now_add=True)
    symptoms = models.TextField(blank=True, null=True)
    status = models.CharField(max_length=50, default='Cleared')

    def __str__(self):
        return f"{self.user.username} - {self.status} on {self.checkin_date.date()}"

class Appointment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='appointments')
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='admin_appointments')
    appointment_date = models.DateTimeField()
    reason_for_visit = models.TextField()
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Appointment for {self.user.username} on {self.appointment_date.date()}"

class DailyLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='daily_logs')
    date = models.DateField(auto_now_add=True)
    mood = models.CharField(max_length=50)
    symptoms = models.JSONField(default=list, blank=True, null=True) # list of strings
    sleep_hours = models.FloatField(default=0.0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"Log for {self.user.username} on {self.date}"

class Announcement(models.Model):
    title = models.CharField(max_length=200)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    image_urls = models.JSONField(default=list, blank=True, null=True) # list of strings
    admin = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='announcements')

    def __str__(self):
        return self.title
