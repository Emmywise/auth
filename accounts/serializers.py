from rest_framework import serializers
from .models import *
from django.contrib import auth
from rest_framework.exceptions import AuthenticationFailed
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
# from django.contrib.auth.models import CustomUser
''' use just the commented userSerializer for normal user creation. new class used to try token out '''

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        # fields = '__all__'
        fields = ('id', 'username', 'email')


class RegisterSerializer(serializers.ModelSerializer):
  
    class Meta:
        model = User
        # fields = '__all__'
        fields = ('id', 'username', 'email', 'password')
        extra_kwargs = {'password': {'write_only':True}}

    def validate(self, attrs):
        email = attrs.get('email', '')
        username = attrs.get('username', '')
        return attrs

    def create(self, validated_data, *args):
        # user = User.object.create_user(validated_data['username'], validated_data['email'], validated_data['password'])
        # user = CustomUser.objects.create_user(validated_data['email'], validated_data['password'])
        user = User.objects.create_user(**validated_data)
        return user

class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)

    class Meta:
        model = User
        fields = ['token']

class LoginSerializer(serializers.ModelSerializer):
    email=serializers.EmailField(max_length=255, min_length=3)
    password=serializers.CharField(max_length=68, min_length=6, write_only=True)
    username=serializers.CharField(max_length=255, min_length=3, read_only=True)
    tokens=serializers.CharField(max_length=68, min_length=6, read_only=True)

    
    class Meta:
        model = User
        fields = ['username','email', 'password', 'tokens']
            
    def validate(self, attrs):
        email = attrs.get('email', '')
        password = attrs.get('password', '')


        user = auth.authenticate(email=email, password=password)
        if not user:
            raise AuthenticationFailed('invalid credientials')
        if not user.is_active:
            raise AuthenticationFailed('account disabled, contact admin')
        if not user.is_verified:
            raise AuthenticationFailed('email not verified')
        
        return {
            'email': user.email,
            'username': user.username,
            'tokens':user.tokens
        }
        return super().validate(attrs)



class LogoutSerializer(serializers.Serializer):
    refresh = serializers.CharField()

    def validate(self, attrs):
        self.token = attrs ['refresh']
        return attrs

    def save(self, **kwargs):

        try:
            RefreshToken(self.token).blacklist()
        
        except TokenError:

            self.fail('bad token')


# class UserSerializer(serializers.ModelSerializer):

#     class Meta:
#         model = CustomUser
#         fields = '__all__'


# class adminLoginForm(forms.Form):
#     email = forms.EmailField()
#     password = forms.CharField(widget=forms.PasswordInput())
#     class Meta:
#         model = CustomUser
#         field =('email', 'password', )
