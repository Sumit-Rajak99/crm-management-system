from rest_framework.routers import DefaultRouter

from .views import (
    LoginViewSet,
    LeadViewSet,
    CallViewSet,
    FollowUpViewSet,
    ConversionViewSet,
    NewEmployeeViewSet,
)

router = DefaultRouter()

router.register(r'login', LoginViewSet, basename='login')
router.register(r'leads', LeadViewSet, basename='lead')
router.register(r'calls', CallViewSet, basename='call')
router.register(r'follow-ups', FollowUpViewSet, basename='follow-up')
router.register(r'conversions', ConversionViewSet, basename='conversion')
router.register(r'employees', NewEmployeeViewSet, basename='employee')

urlpatterns = router.urls