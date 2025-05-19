"""
URL configuration for dbhotel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin # type: ignore
from django.urls import path, include # type: ignore
from accounts import views # type: ignore
from accounts.views  import UserDetailsView
from rest_framework.authtoken.views import obtain_auth_token
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from reservations.views import cancel_reservation


urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/auth/signup/', views.signup, name='signup'),
    path('api/user-profile/', views.get_user_profile, name='user-profile'),
    path('api/user/details/', UserDetailsView.as_view(), name='user_details'),
    path('api/auth/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('', include('accounts.urls')),
    path('', include('rooms.urls')),
    path('', include('reservations.urls')),
    path('api-token-auth/', obtain_auth_token),
    path('api/', include('reservations.urls')),
    path('api/user-profile/', views.UserDetailsView.as_view(), name='user-profile'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/cancel-reservation/', cancel_reservation, name='cancel-reservation'),
]
