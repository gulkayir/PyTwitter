from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from rest_framework_simplejwt.views import TokenObtainPairView

from .views import RegistrationView, ActivationView, ResetPassword, ResetComplete, LogoutView, LoginView, \
    FollowUnfollowView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('refresh/', jwt_views.TokenRefreshView.as_view()),
    path('register/', RegistrationView.as_view()),
    path('activate/<str:activation_code>/', ActivationView.as_view()),
    path('reset-password/', ResetPassword.as_view()),
    path('reset-password-complete/', ResetComplete.as_view()),
    path('follow_unfollow/',FollowUnfollowView.as_view()),
]
