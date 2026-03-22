from rest_framework import serializers
from .models import Role, User, HealthProfile, HealthUpdate, Appointment, DailyLog, Announcement

class RoleSerializer(serializers.ModelSerializer):
    class Meta:
        model = Role
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'student_id', 'role', 'program', 'requires_password_change']

class HealthProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthProfile
        fields = '__all__'
        read_only_fields = ['user']

class HealthUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = HealthUpdate
        fields = '__all__'
        read_only_fields = ['user']

class AppointmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Appointment
        fields = '__all__'
        read_only_fields = ['user']

class DailyLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = DailyLog
        fields = '__all__'
        read_only_fields = ['user']

class AnnouncementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Announcement
        fields = '__all__'
