from django.shortcuts import render, get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.permissions import IsAuthenticated,AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Student, UserToken
from .serializers import StudentSerializer, RegisterSerializer, LoginSerializer

class StudentAPIview(APIView):
    authentication_classes = []
    permission_classes = [AllowAny]
    

    def get(self, request, pk=None):
        if pk:
            stu = get_object_or_404(Student, pk=pk)
            serializer = StudentSerializer(stu)
        else:
            stu = Student.objects.all()
            serializer = StudentSerializer(stu, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        serializer = StudentSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        stu = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(stu, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, pk):
        stu = get_object_or_404(Student, pk=pk)
        serializer = StudentSerializer(stu, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        stu = get_object_or_404(Student, pk=pk)
        stu.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

class RegisterAPIview(APIView):
    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
    {"msg": "Registration is successful", "data": serializer.data}, 
    status=status.HTTP_201_CREATED
)

        return Response({'status': False, 'errors': serializer.errors}, status=status.HTTP_400_BAD_REQUEST)

class LoginApiView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data['username']
            password = serializer.validated_data['password']
            user = authenticate(username=username, password=password)
            if user:
                refresh = RefreshToken.for_user(user)
                access_token= str(refresh.access_token)
                refresh_token = str(refresh)
                # Store values into a database
                UserToken.objects.update_or_create(
            user=user,
            defaults={'refresh_token': refresh_token,'access':access_token} )

             # store values into a data base
                return Response({
                    'refresh': refresh_token,
                    'access': access_token
                      },status=status.HTTP_200_OK)
            return Response({"status": False, "message": "Invalid username or password"}, status=status.HTTP_401_UNAUTHORIZED)
        return Response({"status": False, "data": serializer.errors, "message": "Invalid credentials"}, status=status.HTTP_400_BAD_REQUEST)
