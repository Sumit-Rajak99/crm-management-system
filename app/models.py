from django.db import models
from django.core.validators import MinLengthValidator, RegexValidator


# Employee / Manager Login
class Login(models.Model):

    email = models.EmailField(
        max_length=254,
        
    )
    

    password = models.CharField(
        max_length=128,
        validators=[
            MinLengthValidator(
                8,
                message="Password must be at least 8 characters long."
            ),
            RegexValidator(
                regex=r'^(?=.*[A-Za-z])(?=.*\d).+$',
                message="Password must contain at least one letter and one number."
            )
        ]
    )


# Lead / Customer

class Lead(models.Model):

    STATUS_CHOICES = (
        ('new', 'New'),
        ('contacted', 'Contacted'),
        ('interested', 'Interested'),
        ('follow_up', 'Follow Up'),
        ('converted', 'Converted'),
        ('not_interested', 'Not Interested'),
        ('lost', 'Lost'),
    )

    name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z ]+$',
                message='Name should contain only alphabets and spaces.'
            )
        ]
    )

    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{10}$',
                message='Phone number must contain exactly 10 digits.'
            )
        ]
    )

    email = models.EmailField(
        blank=True
    )

    source = models.CharField(
        max_length=100
    )

    course_interested = models.CharField(
        max_length=100
    )

    assigned_to = models.ForeignKey(
        Login,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name='assigned_leads'
    )

    status = models.CharField(
        max_length=30,
        choices=STATUS_CHOICES,
        default='new'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return self.name
# Call History
from django.db import models


class Call(models.Model):

    CALL_TYPE_CHOICES = (
        ('incoming', 'Incoming'),
        ('outgoing', 'Outgoing'),
    )

    OUTCOME_CHOICES = (
        ('connected', 'Connected'),
        ('not_connected', 'Not Connected'),
        ('busy', 'Busy'),
        ('interested', 'Interested'),
        ('not_interested', 'Not Interested'),
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='calls'
    )

    employee = models.ForeignKey(
        Login,
        on_delete=models.CASCADE,
        related_name='calls'
    )

    call_type = models.CharField(
        max_length=20,
        choices=CALL_TYPE_CHOICES,
        default='outgoing'
    )

    outcome = models.CharField(
        max_length=30,
        choices=OUTCOME_CHOICES,
        default='not_connected'
    )

    call_datetime = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.lead.name} - {self.call_type}"
    # Duration in seconds
    duration = models.PositiveIntegerField(default=0)

    outcome = models.CharField(
        max_length=30,
        choices=OUTCOME_CHOICES
    )

    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.lead.name} - {self.outcome}"


# Follow Up
from django.db import models
from django.core.validators import RegexValidator


class FollowUp(models.Model):

    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )

    lead = models.ForeignKey(
        Lead,
        on_delete=models.CASCADE,
        related_name='follow_ups'
    )

    employee = models.ForeignKey(
        Login,
        on_delete=models.CASCADE,
        related_name='follow_ups'
    )

    follow_up_type = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z ]+$',
                message='Follow-up type should contain only alphabets and spaces.'
            )
        ]
    )

    remarks = models.TextField(
        blank=True
    )

    next_follow_up_date = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    def __str__(self):
        return f"{self.lead.name} - {self.status}"
# Conversion
class Conversion(models.Model):
    

    lead = models.OneToOneField(
        Lead,
        on_delete=models.CASCADE,
        related_name='conversion'
    )

    converted_by = models.ForeignKey(
        Login,
        on_delete=models.SET_NULL,
        null=True,
        related_name='conversions'
    )

    converted_date = models.DateTimeField(
        auto_now_add=True
    )

    course = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9 .&+-]+$',
                message='Course name contains invalid characters.'
            )
        ]
    )

    remarks = models.TextField(
        blank=True
    )

    def __str__(self):
        return f"{self.lead.name} - Converted"
    
# Employee Details
class NewEmployee(models.Model):

    ROLE_CHOICES = (
        ('employee', 'Employee'),
        ('manager', 'Manager'),
        ('admin', 'Admin'),
    )

    login = models.OneToOneField(
    Login,
    on_delete=models.SET_NULL,
    related_name='employee_profile',
    null=True,
    blank=True
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z0-9_-]+$',
                message='Employee ID can contain only letters, numbers, hyphen and underscore.'
            )
        ]
    )

    full_name = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z ]+$',
                message='Full name should contain only alphabets and spaces.'
            )
        ]
    )

    phone = models.CharField(
        max_length=10,
        validators=[
            RegexValidator(
                regex=r'^[0-9]{10}$',
                message='Phone number must contain exactly 10 digits.'
            )
        ]
    )

    department = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z ]+$',
                message='Department should contain only alphabets and spaces.'
            )
        ]
    )

    designation = models.CharField(
        max_length=100,
        validators=[
            RegexValidator(
                regex=r'^[A-Za-z ]+$',
                message='Designation should contain only alphabets and spaces.'
            )
        ]
    )

    role = models.CharField(
        max_length=20,
        choices=ROLE_CHOICES,
        default='employee'
    )

    joining_date = models.DateField()

    is_active = models.BooleanField(
        default=True
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.employee_id} - {self.full_name}"