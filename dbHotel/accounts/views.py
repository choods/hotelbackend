from django.contrib.auth import authenticate, get_user_model
from django.contrib.auth.models import User
from django.contrib.auth.tokens import default_token_generator
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.core.mail import send_mail
from django.conf import settings
from django.urls import reverse
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView  
from rest_framework.response import Response
from rest_framework import status    
from .models import Profile
import json
from django.shortcuts import redirect
import random
from .models import PasswordResetOTP


@api_view(['POST'])
@permission_classes([AllowAny])
def request_password_reset(request):
    email = request.data.get('email')
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)

    otp = str(random.randint(100000, 999999))
    PasswordResetOTP.objects.create(user=user, otp=otp)

    send_mail(
        subject='Password Reset OTP',
        message=f'Your OTP is {otp}. It is valid for 10 minutes.',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        fail_silently=False,
    )

    return Response({'message': 'OTP sent to email.'}, status=200)


@api_view(['POST'])
@permission_classes([AllowAny])
def verify_reset_otp(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    try:
        user = User.objects.get(email=email)
        reset_record = PasswordResetOTP.objects.filter(user=user, otp=otp).last()
        if not reset_record or reset_record.is_expired():
            return Response({'error': 'Invalid or expired OTP.'}, status=400)
        return Response({'message': 'OTP verified.'}, status=200)
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)


@api_view(['POST'])
@permission_classes([AllowAny])
def reset_password(request):
    email = request.data.get('email')
    otp = request.data.get('otp')
    new_password = request.data.get('new_password')

    try:
        user = User.objects.get(email=email)
        reset_record = PasswordResetOTP.objects.filter(user=user, otp=otp).last()
        if not reset_record or reset_record.is_expired():
            return Response({'error': 'Invalid or expired OTP.'}, status=400)
        user.set_password(new_password)
        user.save()
        reset_record.delete()  # optionally delete used OTP
        return Response({'message': 'Password reset successful.'})
    except User.DoesNotExist:
        return Response({'error': 'User not found.'}, status=404)


# 🔐 Signup view
@api_view(['POST'])
@permission_classes([AllowAny])
def signup(request):
    username = request.data.get('username')
    email = request.data.get('email')
    password = request.data.get('password')
    phone = request.data.get('phone')

    # Check if user already exists
    if get_user_model().objects.filter(username=username).exists():
        return Response({'error': 'Username already exists'}, status=400)
    if get_user_model().objects.filter(email=email).exists():
        return Response({'error': 'Email already exists'}, status=400)

    # Create the user
    user = get_user_model().objects.create_user(username=username, email=email, password=password)
    user.is_active = False  # Set the user as inactive until email is verified
    user.save()

    # Create the user's profile
    profile, _ = Profile.objects.get_or_create(user=user)
    profile.phone_number = phone
    profile.save()

    # Generate token for email verification
    token = default_token_generator.make_token(user)
    uid = urlsafe_base64_encode(force_bytes(user.pk))

    # Build the activation URL
    activation_url = request.build_absolute_uri(
        reverse('activate-account', kwargs={'uidb64': uid, 'token': token})
    )

    # HTML content for the email
    html_message = f"""
        <p>Welcome to our platform! Please click the button below to activate your account:</p>
        <a href="{activation_url}" style="display: inline-block; background-color: #007BFF; color: white; padding: 10px 20px; text-align: center; text-decoration: none; border-radius: 5px;">
            Activate Your Account
        </a>
        <p>If the button doesn't work, you can also <a href="{activation_url}">click here</a> to activate your account.</p>
    """

    # Send email with HTML content
    send_mail(
        subject='Activate Your Account',
        message='',
        from_email=settings.DEFAULT_FROM_EMAIL,
        recipient_list=[email],
        html_message=html_message,
        fail_silently=False,
    )

    return Response({'message': 'User created. Please check your email to activate your account.'})

# 📩 Activation view (auto activates the account)
@api_view(['GET'])
@permission_classes([AllowAny])
def activate_account(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = get_user_model().objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        return Response({'error': 'Invalid activation link.'}, status=400)

    if default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        # Redirect to the main application (http://localhost:8081/)
        return redirect('http://localhost:8081/')  # Redirect after activation
    else:
        return Response({'error': 'Activation link is invalid or expired.'}, status=400)




@csrf_exempt
def login(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        username = data.get('username')
        password = data.get('password')

        if not username or not password:
            return JsonResponse({'error': 'Username and password are required.'}, status=400)

        # Authenticate user
        user = authenticate(username=username, password=password)

        if user:
            # Check if the account is active
            if not user.is_active:
                return JsonResponse({'error': 'Please verify your email before logging in.'}, status=403)

            # Generate tokens (JWT)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            refresh_token = str(refresh)

            return JsonResponse({
                'access_token': access_token,
                'refresh_token': refresh_token,
            }, status=200)
        else:
            return JsonResponse({'error': 'Invalid credentials'}, status=400)

    return JsonResponse({'error': 'Invalid request method, POST required.'}, status=405)


# 👤 Get authenticated user details
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_details(request):
    user = request.user
    user_details = {
        "name": user.get_full_name(),
        "email": user.email,
        "phone": user.profile.phone_number if hasattr(user, 'profile') else 'N/A',
    }
    return JsonResponse(user_details)


# 📱 Get profile info
@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_user_profile(request):
    try:
        user = request.user
        profile = Profile.objects.get(user=user)
        data = {
            'username': user.username,
            'email': user.email,
            'phone': profile.phone_number if profile else 'N/A',
        }
        return JsonResponse(data, status=200)
    except Profile.DoesNotExist:
        return JsonResponse({'error': 'Profile not found'}, status=404)


# 🔍 Alternative class-based user detail view
class UserDetailsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        user_data = {
            'username': user.username,
            'email': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
        }
        return JsonResponse(user_data, status=200)
