from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import LoginSerializer, RegisterSerializer, EmailVerificationSerializer,LogoutSerializer
from rest_framework.response import Response
from rest_framework import status, generics, permissions, views
import random
from .models import *
from django.contrib.auth import authenticate, login, logout 
from knox.models import AuthToken
from knox.views import LoginView as KnoxLoginView
from rest_framework.permissions import IsAuthenticated
from rest_framework_simplejwt.tokens import RefreshToken
from .utils import Util
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
import jwt
from django.conf import settings
from drf_yasg.utils import swagger_auto_schema
from drf_yasg import openapi
from rest_framework_simplejwt.authentication import JWTAuthentication


class RegisterView(generics.GenericAPIView):
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_data = serializer.data
        user = User.objects.get(email=user_data['email'])

        token = RefreshToken.for_user(user).access_token

        current_site=get_current_site(request).domain
        relativeLink = reverse('email-verify')
        
        absurl = 'http://'+current_site+relativeLink+"?token="+str(token)
        email_body = 'HI'+user.username+'use link below to verify your email \n'+ absurl
        data = {'email_body': email_body, 'to_email': user.email, 'email_subject': 'verify your email'}

        Util.send_email(data)

        return Response(user_data, status=status.HTTP_201_CREATED)


class verifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer
    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)
    
    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token =request.GET.get('token')
        try:
            auth = JWTAuthentication()
            result =auth.get_validated_token(token)
            user = User.objects.get(id=result['user_id']) 
            if not user.is_verified:
                user.is_verified= True
                user.save()
            return Response({'email': 'successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        
class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer= self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('successfully logout', status=status.HTTP_200_OK)
