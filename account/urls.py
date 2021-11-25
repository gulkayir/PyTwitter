from django.urls import path
from rest_framework_simplejwt import views as jwt_views
from .views import RegistrationView, ActivationView, ResetPassword, ResetComplete, LogoutView, LoginView

urlpatterns = [
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('token/refresh/', jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('register/', RegistrationView.as_view()),
    path('activate/<str:activation_code>/', ActivationView.as_view()),
    path('forgot-password/', ResetPassword.as_view()),
    path('forgot-password-complete/<str:activation_code>/', ResetComplete.as_view()),
]