import json
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from .serializers import UserRegisterSerializer, VerifyOtpSerializer, UserRegisterVerifySerializer, LoginSerializer, ShowinfoSerializer, ManageUserSerializer
from .two_factor import verify_otp
from .models import User
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate, login
from rest_framework.permissions import IsAuthenticated


class RegisterView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        response = serializer.register()
        request.session['data'] = request.data
        return Response(json.loads(response.text), status=status.HTTP_201_CREATED)


class VerifyRegisterOtpView(APIView):
    serializer_class = VerifyOtpSerializer

    def post(self, request, session_id, format=None):
        data = request.data
        serializer = self.serializer_class(data=data)
        serializer.is_valid(raise_exception=True)
        session = request.session['data']
        response = verify_otp(session_id, data['otp'])
        if response.status_code == 200:
            user_serializer = UserRegisterVerifySerializer(data=session)
            user_serializer.is_valid(raise_exception=True)
            user_serializer.save()
            return Response({"message": "Register successfully"}, status=status.HTTP_201_CREATED)
        else:
            return Response(json.loads(response.text), status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            email = serializer.data.get('email')
            password = serializer.data.get('password')
            user = authenticate(email=email, password=password)
            user_serializer = ShowinfoSerializer(user)
            if user is not None:
                login(request, user)
                token = RefreshToken.for_user(user)
                data = {
                    'refresh': str(token),
                    "access": str(token.access_token),
                    'user_serializer': user_serializer.data
                }
                return Response(data)
            return Response({'message':'Invalid email or password!!'}, status=status.HTTP_400_BAD_REQUEST)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class ManageUserView(APIView):
    serializer_class = ManageUserSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request, format=None):
        user = User.objects.all()
        serializer = self.serializer_class(user, many=True)
        return Response(serializer.data)
    
    def delete(self, request, id, format=None):
        if request.user.is_superuser:
            user = User.objects.get(id=id)
            user.delete()
            return Response({"message": "User Deleted"},status=status.HTTP_204_NO_CONTENT)
        return Response({'message':'You dont have permisssion to delete user'}, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request):
        user = request.user
        serializer = self.serializer_class(user, data=request.data) 
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
