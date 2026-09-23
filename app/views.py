# from django.shortcuts import render

# # Create your views here.
from rest_framework.viewsets import ModelViewSet



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from .excel_utils import save_lead_to_excel
from .models import Login
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


from .models import Lead, Call, FollowUp, Conversion, NewEmployee
from .serializers import (
    LeadSerializer,
    CallSerializer,
    FollowUpSerializer,
    ConversionSerializer,
    NewEmployeeSerializer
)

from .excel_utils import (
    save_lead_to_excel,
    save_call_to_excel,
    save_followup_to_excel,
    save_conversion_to_excel,
    save_employee_to_excel
)



# Login ViewSet
# class LoginViewSet(ModelViewSet):
#     queryset = Login.objects.all()
#     serializer_class = LoginSerializer

class LoginAPIView(APIView):

    def post(self, request):

        print("REQUEST DATA:", request.data)

        email = request.data.get("email")
        password = request.data.get("password")

        print("EMAIL:", email)
        print("PASSWORD:", password)

        user = Login.objects.filter(email=email).first()

        print("USER:", user)

        if not user:
            return Response(
                {"message": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        if user.password != password:
            return Response(
                {"message": "Invalid email or password"},
                status=status.HTTP_401_UNAUTHORIZED
            )

        refresh = RefreshToken()

        refresh["user_id"] = user.id
        refresh["email"] = user.email

        return Response({
            "message": "Login successful",
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        })# Lead ViewSet
# class LeadViewSet(ModelViewSet):
#     queryset = Lead.objects.all()
#     serializer_class = LeadSerializer



# Lead ViewSet
class LeadViewSet(ModelViewSet):
    queryset = Lead.objects.all()
    serializer_class = LeadSerializer

    def perform_create(self, serializer):
        lead = serializer.save()
        save_lead_to_excel(lead)


# Call ViewSet
class CallViewSet(ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def perform_create(self, serializer):
        call = serializer.save()
        save_call_to_excel(call)


# Follow Up ViewSet
class FollowUpViewSet(ModelViewSet):
    queryset = FollowUp.objects.all()
    serializer_class = FollowUpSerializer

    def perform_create(self, serializer):
        followup = serializer.save()
        save_followup_to_excel(followup)


# Conversion ViewSet
class ConversionViewSet(ModelViewSet):
    queryset = Conversion.objects.all()
    serializer_class = ConversionSerializer

    def perform_create(self, serializer):
        conversion = serializer.save()
        save_conversion_to_excel(conversion)


# Employee ViewSet
class NewEmployeeViewSet(ModelViewSet):
    queryset = NewEmployee.objects.all()
    serializer_class = NewEmployeeSerializer

    def perform_create(self, serializer):
        employee = serializer.save()
        save_employee_to_excel(employee)

    def list(self, request, *args, **kwargs):
        employees = NewEmployee.objects.all()

        serializer = self.get_serializer(employees, many=True)

        total_employees = employees.count()
        active_employees = employees.filter(is_active=True).count()
        inactive_employees = employees.filter(is_active=False).count()

        return Response({
            "total_employees": total_employees,
            "active_employees": active_employees,
            "inactive_employees": inactive_employees,
            "employees": serializer.data
        })