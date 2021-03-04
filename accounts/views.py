from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import UserSerializer, LoginSerializer, RegisterSerializer, EmailVerificationSerializer,LogoutSerializer
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

#from verify_email.email_handler import send_verification_email
# Create your views here.


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

        # user = serializer.save()
        # return Response({
        #     "user": UserSerializer(user, context=self.get_serializer_context()).data,
        #     "token": AuthToken.objects.create(user)[1]
        # })
class verifyEmail(views.APIView):
    serializer_class = EmailVerificationSerializer


    token_param_config = openapi.Parameter('token', in_=openapi.IN_QUERY, description='Description', type=openapi.TYPE_STRING)

    @swagger_auto_schema(manual_parameters=[token_param_config])
    def get(self, request):
        token =request.GET.get('token')
        print('token:', token)
        print('key:', settings.SECRET_KEY )
        try:
            auth = JWTAuthentication()
            result =auth.get_validated_token(token)
            print('result:', result)

            # payload = jwt.decode(token, settings.SECRET_KEY) 
            # print('payload:', payload)       
            
        
            user = User.objects.get(id=result['user_id'])
            
            print ('user', user)
            print ('id', id)
            
            if not user.is_verified:
                user.is_verified= True
                user.save()
            return Response({'email': 'successfully activated'}, status=status.HTTP_200_OK)
        except jwt.ExpiredSignatureError as identifier:
            return Response({'error': 'Activation Expired'}, status=status.HTTP_400_BAD_REQUEST)
        except jwt.exceptions.DecodeError as identifier:
            return Response({'error': 'Invalid token'}, status=status.HTTP_400_BAD_REQUEST)

        
# class UserAccounts(APIView):

    # def post(self, request):
    #     if request.method == 'POST':
    #         serializer = UserSerializer(data=request.data)
    #         if serializer.is_valid():
    #             obj = serializer.save()
    #             obj.is_active = False
    #             otp = random.randint(1000, 9999)
    #             print ("otp:", otp)
    #             #user = CustomUser.objects.get(id=obj['id'])
    #             user = CustomUser.objects.get(id=serializer.data['id'])
    #             return  Response(serializer.data, status=status.HTTP_201_CREATED)
    #         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    # def get(self, request, pk=None, format=None):
    #     get_users = self.get_object()
    #     serializer = UserSerializer(get_users)
    #     return Response(serializer.data)

    
    # def get(self, request, objects,  pk=None):
    #     get_users = UserAccounts.objects.all()
    #     serializer = UserSerializer(get_users, many=True)
    #     return Response(serializer.data)

class LoginAPIView(generics.GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.data, status=status.HTTP_200_OK)




# class UserLogin(KnoxLoginView):
#     # permissions_classes = (permissions.AllowAny,)
#     permission_classes = (IsAuthenticated,) 
#     # authentication_classes = (TokenAuthentication,) 

#     def post(self, request, format=None):
#         serializer = AuthTokenserializer(data=request.data)
#         serializer.is_valid(raise_exception=True)
#         user = serializer.validated_data['user']
#         login(request, user)
#         return super(UserLogin, self).post(request, format=None)



# class UserLogin(APIView):
#     def post(self, request):
        
#         serializer = LoginSerializer(data=request.data)
#         if request.method == "POST":
#             data = {}
#             email = request.POST.get('email')
#             password = request.POST.get('password')
#             user= authenticate(email=email, password=password) #fetch emial and password correspond from db
#             if user:
#                 if user.is_active:
#                     login(request,user)
#                     return Response("succefully loggedin", status=status.HTTP_201_CREATED)
            
#             return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        #     else:
    #         return Response("Invalid login details given")
        # else:
        #     return render(request, 'dash/login.html', {'form': form})

class LogoutAPIView(generics.GenericAPIView):
    serializer_class = LogoutSerializer

    permission_classes = (permissions.IsAuthenticated,)

    def post(self, request):
        serializer= self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response('successfully logout', status=status.HTTP_200_OK)

# class UserLogout(APIView):

#     def post(self, request):
#         logout(request)
#         return Response("succefully logged out", status=status.HTTP_400_BAD_REQUEST)
