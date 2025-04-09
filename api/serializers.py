from rest_framework import serializers
from api.models import Student
from django.contrib.auth.models import User
class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model=Student
        fields='__all__'

class RegisterSerializer(serializers.ModelSerializer):
    class Meta:  
        model = User
        fields = ['username', 'password']

    def create(self, validated_data):  
        user = User.objects.create_user(**validated_data  # Password is automatically hashed
            # username=validated_data['username'],
            # password=validated_data['password']  # Password is automatically hashed
        )
        return user
    
class LoginSerializer(serializers.Serializer):
    username=serializers.CharField()
    password=serializers.CharField()
