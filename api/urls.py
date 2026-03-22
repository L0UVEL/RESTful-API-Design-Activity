from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework_nested import routers
from .views import (
    RoleViewSet, UserViewSet, HealthProfileViewSet,
    HealthUpdateViewSet, AppointmentViewSet, DailyLogViewSet,
    AnnouncementViewSet, StudentViewSet, SummaryView
)

# Top level routers
router = DefaultRouter(trailing_slash=False)
router.register(r'roles', RoleViewSet, basename='roles')
router.register(r'users', UserViewSet, basename='users')
router.register(r'students', StudentViewSet, basename='students')
router.register(r'appointments', AppointmentViewSet, basename='all-appointments')
router.register(r'announcements', AnnouncementViewSet, basename='announcements')

# Nested routers under users
users_router = routers.NestedSimpleRouter(router, r'users', lookup='user')
users_router.register(r'health-profile', HealthProfileViewSet, basename='user-health-profile')
users_router.register(r'health-updates', HealthUpdateViewSet, basename='user-health-updates')
users_router.register(r'appointments', AppointmentViewSet, basename='user-appointments')
users_router.register(r'daily-logs', DailyLogViewSet, basename='user-daily-logs')

# Nested routers under students
students_router = routers.NestedSimpleRouter(router, r'students', lookup='user')
students_router.register(r'health-profile', HealthProfileViewSet, basename='student-health-profile')
students_router.register(r'health-updates', HealthUpdateViewSet, basename='student-health-updates')
students_router.register(r'appointments', AppointmentViewSet, basename='student-appointments')
students_router.register(r'daily-logs', DailyLogViewSet, basename='student-daily-logs')

urlpatterns = [
    path('summary', SummaryView.as_view(), name='api-summary'),
    path('', include(router.urls)),
    path('', include(users_router.urls)),
    path('', include(students_router.urls)),
]
