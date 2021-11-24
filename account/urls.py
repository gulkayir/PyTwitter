from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView


from .views import *

urlpatterns = [
    path('register/', RegistrationView.as_view()),
    path('activation/<str:activation_code>/', ActivateView.as_view()),
    path('login/', LoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('refresh/', TokenRefreshView.as_view()),
    path('reset_password/', ResetPassword.as_view()),
    path('reset_complete/', ResetComplete.as_view()),
]