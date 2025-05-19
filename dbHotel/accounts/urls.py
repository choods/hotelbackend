from django.urls import path # type: ignore
from . import views
from .views import signup, activate_account, login

urlpatterns = [
    path('api/signup/', views.signup, name='signup'),
    path('api/login/', views.login, name='login'),
    path('api/user-profile/', views.UserDetailsView.as_view(), name='user-profile'),
    path('activate/<uidb64>/<token>/', activate_account, name='activate-account'),

    path('api/request-password-reset/', views.request_password_reset, name='request-password-reset'),
    path('api/verify-reset-otp/', views.verify_reset_otp, name='verify-reset-otp'),
    path('api/reset-password/', views.reset_password, name='reset-password'),
    ]
