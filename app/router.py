from .views import ExecutiveDashboardAPIView
from rest_framework.routers import DefaultRouter


from rest_framework.routers import DefaultRouter
from django.urls import path

from .views import (
    LeadViewSet,
    CallViewSet,
    FollowUpViewSet,
    ConversionViewSet,
    NewEmployeeViewSet,
    ExecutiveDashboardAPIView,
    ExecutiveMyLeadsAPIView,
    ExecutiveMyCallsAPIView,
    ExecutiveMyFollowUpsAPIView,
    ExecutiveProfileAPIView,
)

router = DefaultRouter()

router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'calls', CallViewSet, basename='call')
router.register(r'follow-ups', FollowUpViewSet, basename='follow-up')
router.register(r'conversions', ConversionViewSet, basename='conversion')
router.register(r'employees', NewEmployeeViewSet, basename='employee')

urlpatterns = router.urls

# Executive Dashboard API
urlpatterns += [
    path(
        "executive/dashboard/",
        ExecutiveDashboardAPIView.as_view(),
        name="executive-dashboard",
    ),

    path(
    "executive/dashboard/",
    ExecutiveDashboardAPIView.as_view(),
    name="executive-dashboard",
),
    path(
         "executive/my-leads/",
         ExecutiveMyLeadsAPIView.as_view(),
         name="executive-my-leads",
),

    path(
    "executive/my-calls/",
    ExecutiveMyCallsAPIView.as_view(),
    name="executive-my-calls",
),

path(
    "executive/my-follow-ups/",
    ExecutiveMyFollowUpsAPIView.as_view(),
    name="executive-my-follow-ups",
),

path(
    "executive/profile/",
    ExecutiveProfileAPIView.as_view(),
    name="executive-profile",
),

]