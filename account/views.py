from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.views import APIView
from . utils import send_activation_code
from account.serializers import RegisterSerializer, LoginSerializer, ResetPasswordSerializer

User = get_user_model()


class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully registered. Check your email to confirm', status=status.HTTP_201_CREATED)


class ActivateView(APIView):
    def get(self, request, activation_code):
        user = get_object_or_404(User, activation_code=activation_code)
        user.is_active = True
        user.activation_code = ''
        user.save()
        return Response('Your account successfully activated! ', status=status.HTTP_200_OK)


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer


class LogoutView(APIView):
    permission_classes = [IsAuthenticated, ]

    def post(self, request):
        user = request.user
        Token.objects.filter(user=user).delete()
        return Response('Successfully logget out', status=status.HTTP_200_OK)


class ResetPassword(APIView):
    def get(self, request):
        email = request.query_params.get('email')
        user = get_object_or_404(User, email=email)
        user.is_active = False
        user.create_activation_code()
        user.save()
        send_activation_code.delay(user.email, user.activation_code)
        return Response('Email sent', status=status.HTTP_200_OK)


class ResetComplete(APIView):
    def post(self, request):
        serializer = ResetPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('You successfully reseted your password ', status=status.HTTP_200_OK)


