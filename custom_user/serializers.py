
from enum import unique
from django.db.models import fields
from rest_framework import serializers

from .validate_class import AgeAtLeast18
from .models import CustomUser

class UserSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=100),
    first_name = serializers.CharField(),
    age = serializers.IntegerField()
    class Meta:
        model = CustomUser
        validators = [AgeAtLeast18()]
        fields = ['email', 'first_name', 'age', 'password']
        extra_kwargs = {
            'password': {'write_only': True},
            'first_name': {'required': True},
            'email': {'required': True}
        }

    def create(self, validated_data):
        user = CustomUser(
            email=validated_data['email'],
            first_name=validated_data['first_name'],
            age=validated_data['age']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user
    def save(self, request):
        # email=request.data['email'],
        # first_name=request.data['first_name'],
        # age=request.data['age']
        email = self.validated_data['email']
        first_name = self.validated_data['first_name']
        age = self.validated_data['age']
        user = CustomUser(
            email=email,
            first_name=first_name,
            age=age
        )
        user.set_password(self.validated_data['password'])
        user.save()
        return user
    