# from django.shortcuts import render

# # Create your views here.
from rest_framework.viewsets import ModelViewSet



from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.decorators import action
from rest_framework_simplejwt.tokens import RefreshToken
from .excel_utils import save_lead_to_excel
from django.utils import timezone
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









# EXECUTIVE DASHBOARD BACKEND START



class ExecutiveDashboardAPIView(APIView):
    """
    Executive dashboard summary.
    Admin ke existing views ko modify nahi karta.
    """

    def get(self, request):
        today = timezone.localdate()

        total_leads = Lead.objects.count()
        converted_leads = Conversion.objects.count()
        total_calls = Call.objects.count()

        pending_followups = FollowUp.objects.filter(
            status="pending"
        ).count()

        today_followups = FollowUp.objects.filter(
            next_follow_up_date__date=today,
            status="pending"
        ).count()

        conversion_rate = (
            round((converted_leads / total_leads) * 100, 2)
            if total_leads else 0
        )

        return Response({
            "total_leads": total_leads,
            "converted_leads": converted_leads,
            "conversion_rate": conversion_rate,
            "total_calls": total_calls,
            "pending_followups": pending_followups,
            "today_followups": today_followups
        }, status=status.HTTP_200_OK)


# Executive My Leads API

class ExecutiveMyLeadsAPIView(APIView):
    """
    Returns leads assigned to the executive.
    """

    def get(self, request):
        employee_id = request.query_params.get("employee_id")

        if not employee_id:
            return Response(
                {"error": "employee_id is required for testing."},
                status=status.HTTP_400_BAD_REQUEST
            )

        leads = Lead.objects.filter(assigned_to_id=employee_id)

        data = [
            {
                "id": lead.id,
                "name": lead.name,
                "phone": lead.phone,
                "email": lead.email,
                "source": lead.source,
                "course_interested": lead.course_interested,
                "status": lead.status,
            }
            for lead in leads
        ]

        return Response(
            {"total_leads": len(data), "leads": data},
            status=status.HTTP_200_OK
        )




# Executive My Calls API

class ExecutiveMyCallsAPIView(APIView):
    """
    Returns calls for the selected employee.
    """

    def get(self, request):
        employee_id = request.query_params.get("employee_id")

        if not employee_id:
            return Response(
                {"error": "employee_id is required for testing."},
                status=status.HTTP_400_BAD_REQUEST
            )

        calls = Call.objects.filter(employee_id=employee_id).select_related("lead")

        data = [
            {
                "id": call.id,
                "lead_id": call.lead_id,
                "lead_name": call.lead.name,
                "call_type": call.call_type,
                "outcome": call.outcome,
                "duration": call.duration,
                "notes": call.notes,
                "call_datetime": call.call_datetime,
            }
            for call in calls
        ]

        return Response(
            {"total_calls": len(data), "calls": data},
            status=status.HTTP_200_OK
        )    





# Executive My Follow-ups API

class ExecutiveMyFollowUpsAPIView(APIView):
    """
    Returns follow-ups for the selected employee.
    """

    def get(self, request):
        employee_id = request.query_params.get("employee_id")

        if not employee_id:
            return Response(
                {"error": "employee_id is required for testing."},
                status=status.HTTP_400_BAD_REQUEST
            )

        followups = FollowUp.objects.filter(
            employee_id=employee_id
        ).select_related("lead").order_by("next_follow_up_date")

        data = [
            {
                "id": followup.id,
                "lead_id": followup.lead_id,
                "lead_name": followup.lead.name,
                "follow_up_type": followup.follow_up_type,
                "remarks": followup.remarks,
                "next_follow_up_date": followup.next_follow_up_date,
                "status": followup.status,
            }
            for followup in followups
        ]

        return Response(
            {"total_followups": len(data), "followups": data},
            status=status.HTTP_200_OK
        )    
    






# Executive Profile API

class ExecutiveProfileAPIView(APIView):
    """
    Returns employee profile for testing.
    """

    def get(self, request):
        employee_id = request.query_params.get("employee_id")

        if not employee_id:
            return Response(
                {"error": "employee_id is required for testing."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            employee = NewEmployee.objects.get(login_id=employee_id)
        except NewEmployee.DoesNotExist:
            return Response(
                {"error": "Employee profile not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        data = {
            "employee_id": employee.employee_id,
            "full_name": employee.full_name,
            "email": employee.login.email,
            "phone": employee.phone,
            "department": employee.department,
            "designation": employee.designation,
            "role": employee.role,
            "joining_date": employee.joining_date,
            "is_active": employee.is_active,
        }

        return Response(data, status=status.HTTP_200_OK)












# Executive Lead Status Update API
class ExecutiveLeadStatusUpdateAPIView(APIView):

    def patch(self, request, lead_id):
        employee_id = request.query_params.get("employee_id")

        if not employee_id:
            return Response(
                {"error": "employee_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lead = Lead.objects.get(
                id=lead_id,
                assigned_to_id=employee_id
            )
        except Lead.DoesNotExist:
            return Response(
                {"error": "Assigned lead not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        new_status = request.data.get("status")

        valid_statuses = [
            choice[0] for choice in Lead.STATUS_CHOICES
        ]

        if new_status not in valid_statuses:
            return Response(
                {
                    "error": "Invalid status.",
                    "valid_statuses": valid_statuses
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        lead.status = new_status
        lead.save()

        return Response(
            {
                "message": "Lead status updated successfully.",
                "lead_id": lead.id,
                "status": lead.status
            },
            status=status.HTTP_200_OK
        )





# Executive Create Call Log API
class ExecutiveCreateCallAPIView(APIView):

    def post(self, request):
        employee_id = request.query_params.get("employee_id")

        if not employee_id:
            return Response(
                {"error": "employee_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        lead_id = request.data.get("lead_id")

        try:
            lead = Lead.objects.get(
                id=lead_id,
                assigned_to_id=employee_id
            )
        except (Lead.DoesNotExist, ValueError, TypeError):
            return Response(
                {"error": "Assigned lead not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        call_type = request.data.get("call_type", "outgoing")
        outcome = request.data.get("outcome", "not_connected")

        valid_call_types = [
            choice[0] for choice in Call.CALL_TYPE_CHOICES
        ]
        valid_outcomes = [
            choice[0] for choice in Call.OUTCOME_CHOICES
        ]

        if call_type not in valid_call_types:
            return Response(
                {"error": "Invalid call_type."},
                status=status.HTTP_400_BAD_REQUEST
            )

        if outcome not in valid_outcomes:
            return Response(
                {"error": "Invalid outcome."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            duration = int(request.data.get("duration", 0))
            if duration < 0:
                raise ValueError
        except (ValueError, TypeError):
            return Response(
                {"error": "duration must be a non-negative integer."},
                status=status.HTTP_400_BAD_REQUEST
            )

        call = Call.objects.create(
            lead=lead,
            employee_id=employee_id,
            call_type=call_type,
            outcome=outcome,
            duration=duration,
            notes=request.data.get("notes", "")
        )

        return Response(
            {
                "message": "Call log created successfully.",
                "id": call.id,
                "lead_id": call.lead_id,
                "call_type": call.call_type,
                "outcome": call.outcome,
                "duration": call.duration,
                "notes": call.notes
            },
            status=status.HTTP_201_CREATED
        )




# Executive Create Follow-up API
class ExecutiveCreateFollowUpAPIView(APIView):

    def post(self, request):
        employee_id = request.query_params.get("employee_id")

        if not employee_id:
            return Response(
                {"error": "employee_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        lead_id = request.data.get("lead_id")

        try:
            lead = Lead.objects.get(
                id=lead_id,
                assigned_to_id=employee_id
            )
        except (Lead.DoesNotExist, ValueError, TypeError):
            return Response(
                {"error": "Assigned lead not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        follow_up_type = request.data.get("follow_up_type")
        next_date = request.data.get("next_follow_up_date")

        if not follow_up_type or not next_date:
            return Response(
                {
                    "error": (
                        "follow_up_type and next_follow_up_date "
                        "are required."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST
            )

        followup = FollowUp(
            lead=lead,
            employee_id=employee_id,
            follow_up_type=follow_up_type,
            remarks=request.data.get("remarks", ""),
            next_follow_up_date=next_date,
            status="pending"
        )

        try:
            followup.full_clean()
            followup.save()
        except Exception as exc:
            from django.core.exceptions import ValidationError
            from django.utils.dateparse import parse_datetime

            return Response(
                {"error": "Invalid follow-up data. Check the date and type."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "Follow-up created successfully.",
                "id": followup.id,
                "lead_id": followup.lead_id,
                "follow_up_type": followup.follow_up_type,
                "next_follow_up_date": followup.next_follow_up_date,
                "status": followup.status
            },
            status=status.HTTP_201_CREATED
        )






# Executive Update Follow-up API
class ExecutiveUpdateFollowUpAPIView(APIView):

    def patch(self, request, followup_id):
        employee_id = request.query_params.get("employee_id")

        if not employee_id:
            return Response(
                {"error": "employee_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            followup = FollowUp.objects.get(
                id=followup_id,
                employee_id=employee_id
            )
        except (FollowUp.DoesNotExist, ValueError, TypeError):
            return Response(
                {"error": "Follow-up not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        allowed_fields = {
            "status",
            "next_follow_up_date",
            "remarks",
            "follow_up_type"
        }

        updates = {
            key: value
            for key, value in request.data.items()
            if key in allowed_fields
        }

        if not updates:
            return Response(
                {"error": "Provide a valid field to update."},
                status=status.HTTP_400_BAD_REQUEST
            )

        valid_statuses = [
            choice[0] for choice in FollowUp.STATUS_CHOICES
        ]

        if (
            "status" in updates
            and updates["status"] not in valid_statuses
        ):
            return Response(
                {"error": "Invalid follow-up status."},
                status=status.HTTP_400_BAD_REQUEST
            )

        for field, value in updates.items():
            setattr(followup, field, value)

        try:
            followup.full_clean()
            followup.save()
        except Exception:
            return Response(
                {"error": "Invalid follow-up data."},
                status=status.HTTP_400_BAD_REQUEST
            )

        return Response(
            {
                "message": "Follow-up updated successfully.",
                "id": followup.id,
                "status": followup.status,
                "next_follow_up_date": followup.next_follow_up_date,
                "remarks": followup.remarks
            },
            status=status.HTTP_200_OK
        )





# Executive Lead Conversion API
class ExecutiveLeadConversionAPIView(APIView):

    def post(self, request, lead_id):
        employee_id = request.query_params.get("employee_id")

        if not employee_id:
            return Response(
                {"error": "employee_id is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            lead = Lead.objects.get(
                id=lead_id,
                assigned_to_id=employee_id
            )
        except (Lead.DoesNotExist, ValueError, TypeError):
            return Response(
                {"error": "Assigned lead not found."},
                status=status.HTTP_404_NOT_FOUND
            )

        if Conversion.objects.filter(lead=lead).exists():
            return Response(
                {"error": "This lead is already converted."},
                status=status.HTTP_400_BAD_REQUEST
            )

        course = request.data.get("course")
        if not course:
            return Response(
                {"error": "course is required."},
                status=status.HTTP_400_BAD_REQUEST
            )

        conversion = Conversion(
            lead=lead,
            converted_by_id=employee_id,
            course=course,
            remarks=request.data.get("remarks", "")
        )

        try:
            conversion.full_clean()
            conversion.save()
        except Exception:
            return Response(
                {"error": "Invalid conversion data. Check the course name."},
                status=status.HTTP_400_BAD_REQUEST
            )

        lead.status = "converted"
        lead.save(update_fields=["status", "updated_at"])

        return Response(
            {
                "message": "Lead converted successfully.",
                "lead_id": lead.id,
                "conversion_id": conversion.id,
                "status": lead.status,
                "course": conversion.course
            },
            status=status.HTTP_201_CREATED
        )
