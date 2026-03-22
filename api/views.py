from rest_framework import viewsets, mixins
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.views import APIView
from django.shortcuts import get_object_or_404
from .models import Role, User, HealthProfile, HealthUpdate, Appointment, DailyLog, Announcement
from .serializers import (
    RoleSerializer, UserSerializer, HealthProfileSerializer, 
    HealthUpdateSerializer, AppointmentSerializer, 
    DailyLogSerializer, AnnouncementSerializer
)

class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.all()
    serializer_class = RoleSerializer

class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class StudentViewSet(viewsets.ModelViewSet):
    queryset = User.objects.filter(is_staff=False)
    serializer_class = UserSerializer

# For nested routes under /users/{user_pk}/...
class HealthProfileViewSet(viewsets.ModelViewSet):
    serializer_class = HealthProfileSerializer

    def get_queryset(self):
        return HealthProfile.objects.filter(user_id=self.kwargs['user_pk'])

    def perform_create(self, serializer):
        user = get_object_or_404(User, pk=self.kwargs['user_pk'])
        serializer.save(user=user)

class HealthUpdateViewSet(viewsets.ModelViewSet):
    serializer_class = HealthUpdateSerializer

    def get_queryset(self):
        # Allow filtering by status via query param
        qs = HealthUpdate.objects.filter(user_id=self.kwargs['user_pk'])
        status = self.request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

    def perform_create(self, serializer):
        user = get_object_or_404(User, pk=self.kwargs['user_pk'])
        serializer.save(user=user)

class AppointmentViewSet(viewsets.ModelViewSet):
    serializer_class = AppointmentSerializer

    def get_queryset(self):
        # Allow filtering by status
        qs = Appointment.objects.all()
        
        # If accessed via nested router /users/{user_pk}/appointments
        if 'user_pk' in self.kwargs:
            qs = qs.filter(user_id=self.kwargs['user_pk'])
            
        status = self.request.query_params.get('status')
        if status:
            qs = qs.filter(status=status)
        return qs

    def perform_create(self, serializer):
        if 'user_pk' in self.kwargs:
            user = get_object_or_404(User, pk=self.kwargs['user_pk'])
            serializer.save(user=user)
        else:
            serializer.save()

class DailyLogViewSet(viewsets.ModelViewSet):
    serializer_class = DailyLogSerializer

    def get_queryset(self):
        qs = DailyLog.objects.filter(user_id=self.kwargs['user_pk'])
        date = self.request.query_params.get('date')
        if date:
            qs = qs.filter(date=date)
        return qs

    def perform_create(self, serializer):
        user = get_object_or_404(User, pk=self.kwargs['user_pk'])
        serializer.save(user=user)

class AnnouncementViewSet(viewsets.ModelViewSet):
    queryset = Announcement.objects.all().order_by('-timestamp')
    serializer_class = AnnouncementSerializer

class SummaryView(APIView):
    def get(self, request, *args, **kwargs):
        roles = Role.objects.all()
        users = User.objects.all()
        students = User.objects.filter(is_staff=False)
        appointments = Appointment.objects.all()
        announcements = Announcement.objects.all().order_by('-timestamp')

        return Response({
            'roles': RoleSerializer(roles, many=True).data,
            'users': UserSerializer(users, many=True).data,
            'students': UserSerializer(students, many=True).data,
            'appointments': AppointmentSerializer(appointments, many=True).data,
            'announcements': AnnouncementSerializer(announcements, many=True).data,
        })
