from django.contrib.auth import get_user_model
from django.shortcuts import render, get_object_or_404
from rest_framework import status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token

from rest_framework.response import Response
from rest_framework.views import APIView
from .utils import send_activation_code
from account.serializers import RegisterSerializer, LoginSerializer, CreateNewPasswordSerializer

User = get_user_model()


class RegistrationView(APIView):
    def post(self, request):
        data = request.data
        serializer = RegisterSerializer(data=data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Successfully registered. Check your email to confirm', status=status.HTTP_201_CREATED)


class ActivationView(APIView):
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
        try:
            user = User.objects.get(email=email)
            user.is_active = False
            user.create_activation_code()
            user.save()
            send_activation_code(user)
            return Response('Вам отправлено письмо', status=200)
        except User.DoesNotExist:
            return Response({'msg': 'User doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)


class ResetComplete(APIView):
    def post(self, request):
        serializer = CreateNewPasswordSerializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response('Password reseted successfully', status=200)

class FollowUnfollowView(APIView):
    permission_classes = [IsAuthenticated, ]

    def first_profile(self):
        try:
            return User.objects.get(user=self.request.user)
        except User.DoesNotExist:
            return Response('User doesnt exist', status=status.HTTP_400_BAD_REQUEST)

    def second_profile(self, pk):
            try:
                return User.objects.get(id=pk)
            except User.DoesNotExist:
                return Response('User doesnt exist', status=status.HTTP_400_BAD_REQUEST)

    def post(self, request, format=None):
        pk = request.data.get('email')
        req_type = request.data.get('type')

        first_profile = self.first_profile()
        second_profile = self.second_profile(pk)

        if req_type == 'follow':
                first_profile.following.add(second_profile)
                second_profile.followers.add(first_profile)
                return Response({"Following": "Following success!!"}, status=status.HTTP_200_OK)

        elif req_type == 'accept':
            first_profile.followers.add(second_profile)
            second_profile.following.add(first_profile)
            return Response({"Accepted": "Follow request successfuly accespted!!"}, status=status.HTTP_200_OK)

        elif req_type == 'unfollow':
            first_profile.following.remove(second_profile)
            second_profile.followers.remove(first_profile)
            return Response({"Unfollow": "Unfollow success!!"}, status=status.HTTP_200_OK)

        elif req_type == 'remove':
            first_profile.followers.remove(second_profile)
            second_profile.following.remove(first_profile)
            return Response({"Remove Success": "Successfuly removed your follower!!"}, status=status.HTTP_200_OK)

