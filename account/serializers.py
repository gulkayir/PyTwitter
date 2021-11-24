from django.contrib.auth import authenticate
from rest_framework import serializers
from account.utils import send_activation_code
from account.models import User


class RegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(min_length=6, write_only=True)
    password_confirm = serializers.CharField(min_length=6, write_only=True)

    class Meta:
        model = User
        fields = ('email', 'password', 'password_confirm')

    def validate(self, validated_data):
        password = validated_data.get('password')
        password_confirm = validated_data.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Password do not match')
        return validated_data

    def create(self, validated_data):
        email = validated_data.get('email')
        password = validated_data.get('password')
        user = User.objects.create_user(email=email, password=password)
        send_activation_code.delay(email=user.email, activation_code=str(user.activation_code))
        return user

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField(
        label='Password',
        style={'input_type': 'password'},
        trim_whitespace=False
    )

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            if not user:
                message = 'Unable to log in with provided credentials'
                raise serializers.ValidationError(message, code='authorization')

        else:
            message = 'Must include "email" and "password". '
            raise serializers.ValidationError(message, code='authorization')

        attrs['user'] = user
        return attrs

class ResetPasswordSerializer(serializers.Serializer):
    email = serializers.EmailField()
    activation_code = serializers.CharField(max_length=6, min_length=6, required=True)
    password = serializers.CharField(min_length=8, required=True)
    password_confirm = serializers.CharField(min_length=8, required=True)

    def validate_email(self, email):
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError('User with given email does not exists')
        return email

    def validate_activation_code(self, code):
        if not User.objects.filter(activation_coder=code, is_active=False).exists():
            raise serializers.ValidationError('Activation code is invalid!')
        return code

    def validate(self, attrs):
        password = attrs.get('password')
        password_confirm = attrs.get('password_confirm')
        if password != password_confirm:
            raise serializers.ValidationError('Passwords do not match!')
        return attrs

    def save(self, **kwargs):
        data = self.validated_data()
        email = data.get('email')
        code = data.get('code')
        password = data.get('password')
        try:
            user = User.objects.get(email=email, activation_code=code, is_active=False)
        except User.DoesNotExist:
            raise serializers.ValidationError('Пользователь не найден')

        user.is_active = True
        user.activation_code = ''
        user.set_password(password)
        user.save()



# class ShortUserInfoSerializer(serializers.ModelSerializer):
#     """Краткая информауия о пользователе"""
#
#     class Meta:
#         model = User
#         fields = ['id', 'username', 'name', 'avatar']
#         read_only_fields = ['id', 'username', 'name', 'avatar']
#
#
#
# class UserFollowingListSerializer(ShortUserInfoSerializer):
#     """На кого подписан пользователь"""
#     id = serializers.IntegerField(source='following_user_id')
#
#
# class UserFollowersListSerializer(ShortUserInfoSerializer):
#     """Подписчики пользователя"""
#     id = serializers.IntegerField(source='user_id')
#
#
# class FollowSerializer(serializers.ModelSerializer):
#     """Подписка текущего пользователя на другого"""
#     following_user_id = serializers.IntegerField()
#
#     class Meta:
#         model = Following
#         fields = ['following_user_id']
#
#     @transaction.atomic
#     def save(self):
#         user = self.context['request'].user
#         following_user_id = self.validated_data['following_user_id']
#         following_user_obj = get_object_or_404(User, id=following_user_id)
#         if user == following_user_obj:
#             return
#         following = Following.objects.get_or_create(
#             user=user, following_user=following_user_obj)
#         # todo: add signal that user start following
#         return following
#
#
# class UnfollowSerializer(serializers.ModelSerializer):
#     """Отписаться от пользователя"""
#     unfollowing_user_id = serializers.IntegerField(source='following_user_id')
#
#     class Meta:
#         model = Following
#         fields = ['unfollowing_user_id']
#
#     @transaction.atomic
#     def save(self):
#         user = self.context['request'].user
#         unfollowing_user_id = self.validated_data['following_user_id']
#         unfollowing_user_obj = get_object_or_404(User, id=unfollowing_user_id)
#         unfollowing = get_object_or_404(
#             Following, user=user, following_user=unfollowing_user_obj).delete()
#         # todo: add signal that user unfollowing
#         return unfollowing