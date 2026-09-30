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

    def list(self, request, *args, **kwargs):
        leads = Lead.objects.all()

        serializer = self.get_serializer(leads, many=True)

        
        total_leads = leads.count()

        
        new_leads = leads.filter(status="new").count()

        
        positive_leads = leads.filter(status="interested").count()

        
        converted_leads = leads.filter(status="converted").count()
        
        conversion_rate = (
        (converted_leads / total_leads) * 100
        if total_leads > 0 else 0
                        )

        return Response({
            "total_leads": total_leads,
            "conversion_rate": round(conversion_rate, 2),
            "new_leads": new_leads,
            "positive_leads": positive_leads,
            "converted_leads": converted_leads,
            "all_leads": serializer.data
        })

from django.db.models import Avg
# Call ViewSet
class CallViewSet(ModelViewSet):
    queryset = Call.objects.all()
    serializer_class = CallSerializer

    def perform_create(self, serializer):
        call = serializer.save()
        save_call_to_excel(call)

    def list(self, request, *args, **kwargs):
        calls = Call.objects.all()

        serializer = self.get_serializer(calls, many=True)

        total_calls = calls.count()
        completed_calls = calls.filter(status="completed").count()
        scheduled_calls = calls.filter(status="scheduled").count()
        missed_calls = calls.filter(status="missed").count()
        pending_calls = calls.filter(status="pending").count()
        avg_duration = calls.filter(
        duration__isnull=False
        ).aggregate(
            avg=Avg("duration")
        )["avg"] or 0

        avg_duration_minutes = round(avg_duration / 60, 2)

        return Response({
            "total_calls": total_calls,
            "completed_calls": completed_calls,
            "scheduled_calls": scheduled_calls,
            "missed_calls": missed_calls,
            "pending_calls": pending_calls,
            "average_duration_minutes": avg_duration_minutes,
            "calls": serializer.data
        })
        
        

# Follow Up ViewSet
class FollowUpViewSet(ModelViewSet):
    queryset = FollowUp.objects.all()
    serializer_class = FollowUpSerializer

    def perform_create(self, serializer):
        followup = serializer.save()
        save_followup_to_excel(followup)

    def list(self, request, *args, **kwargs):
        followups = FollowUp.objects.all()

        serializer = self.get_serializer(followups, many=True)

        total_followup = followups.count()
        today_followup = followups.filter(status="today").count()
        pending = followups.filter(status="pending").count()
        complete = followups.filter(status="complete").count()
        overdue = followups.filter(status="overdue").count()
        rescheduled = followups.filter(status="rescheduled").count()

        return Response({
            "total_followup": total_followup,
            "today_followup": today_followup,
            "pending": pending,
            "complete": complete,
            "overdue": overdue,
            "rescheduled": rescheduled,
            "followups": serializer.data
        })  


# Conversion ViewSet
class ConversionViewSet(ModelViewSet):
    queryset = Conversion.objects.all()
    serializer_class = ConversionSerializer

    def perform_create(self, serializer):
        conversion = serializer.save()
        save_conversion_to_excel(conversion)

    def list(self, request, *args, **kwargs):
        conversions = Conversion.objects.all()

        serializer = self.get_serializer(conversions, many=True)

        total_leads = Lead.objects.count()

        interested_leads = Lead.objects.filter(
            status="interested"
        ).count()

        converted_leads = Lead.objects.filter(
            status="converted"
        ).count()

        return Response({
            "total_leads": total_leads,
            "interested_leads": interested_leads,
            "converted_leads": converted_leads,
            "conversions": serializer.data
        })

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