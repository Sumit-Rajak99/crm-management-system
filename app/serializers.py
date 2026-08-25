from rest_framework import serializers

from .models import (
    Login,
    Lead,
    Call,
    FollowUp,
    Conversion,
    NewEmployee
)


class LoginSerializer(serializers.ModelSerializer):
    class Meta:
        model = Login
        fields = '__all__'


class LeadSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lead
        fields = '__all__'


class CallSerializer(serializers.ModelSerializer):
    class Meta:
        model = Call
        fields = '__all__'


class FollowUpSerializer(serializers.ModelSerializer):
    class Meta:
        model = FollowUp
        fields = '__all__'


class ConversionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Conversion
        fields = '__all__'


class NewEmployeeSerializer(serializers.ModelSerializer):
    class Meta:
        model = NewEmployee
        fields = '__all__'