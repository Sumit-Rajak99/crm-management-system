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
    ExecutiveLeadStatusUpdateAPIView,
    ExecutiveCreateCallAPIView,
    ExecutiveCreateFollowUpAPIView,
    ExecutiveUpdateFollowUpAPIView,
    ExecutiveLeadConversionAPIView,
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

path(
    "executive/leads/<int:lead_id>/status/",
    ExecutiveLeadStatusUpdateAPIView.as_view(),
    name="executive-lead-status-update",
),
path(
    "executive/my-calls/create/",
    ExecutiveCreateCallAPIView.as_view(),
    name="executive-create-call",
),

path(
    "executive/my-follow-ups/create/",
    ExecutiveCreateFollowUpAPIView.as_view(),
    name="executive-create-follow-up",
),
path(
    "executive/my-follow-ups/<int:followup_id>/",
    ExecutiveUpdateFollowUpAPIView.as_view(),
    name="executive-update-follow-up",
),

path(
    "executive/leads/<int:lead_id>/convert/",
    ExecutiveLeadConversionAPIView.as_view(),
    name="executive-lead-convert",
),

]