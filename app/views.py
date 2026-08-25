from django.shortcuts import render

# Create your views here.
from rest_framework.viewsets import ModelViewSet

from .models import (
    Login,
    Lead,
    Call,
    FollowUp,
    Conversion,
    NewEmployee
)

from .serializers import (
    LoginSerializer,
    LeadSerializer,
    CallSerializer,
    FollowUpSerializer,
    ConversionSerializer,
    NewEmployeeSerializer
)


# Login ViewSet
class LoginViewSet(ModelViewSet):
    queryset = Login.objects.all()
    serializer_class = LoginSerializer


# Lead ViewSet
class LeadViewSet(ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer


# Call ViewSet
class CallViewSet(ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer


# Follow Up ViewSet
class FollowUpViewSet(ModelViewSet):
    queryset = FollowUp.objects.all()
    serializer_class = FollowUpSerializer


# Conversion ViewSet
class ConversionViewSet(ModelViewSet):
    queryset = Conversion.objects.all()
    serializer_class = ConversionSerializer


# Employee ViewSet
class NewEmployeeViewSet(ModelViewSet):
    queryset = NewEmployee.objects.all()
    serializer_class = NewEmployeeSerializer