from django.db import models


# Employee / Manager Login
class Login(models.Model): 
    email = models.EmailField(max_length=254, unique=True)
    password = models.CharField(max_length=128)
    


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

    name = models.CharField(max_length=100)
    phone = models.CharField(max_length=15)
    email = models.EmailField(blank=True)
    source = models.CharField(max_length=100)
    course_interested = models.CharField(max_length=100)

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

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Call History
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

    call_datetime = models.DateTimeField(auto_now_add=True)

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

    follow_up_type = models.CharField(max_length=100)

    remarks = models.TextField(blank=True)

    next_follow_up_date = models.DateTimeField()

    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default='pending'
    )

    created_at = models.DateTimeField(auto_now_add=True)

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

    converted_date = models.DateTimeField(auto_now_add=True)

    course = models.CharField(max_length=100)

    remarks = models.TextField(blank=True)

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
        on_delete=models.CASCADE,
        related_name='employee_profile'
    )

    employee_id = models.CharField(
        max_length=20,
        unique=True
    )

    full_name = models.CharField(max_length=100)

    phone = models.CharField(max_length=15)

    department = models.CharField(
        max_length=100
    )

    designation = models.CharField(
        max_length=100
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