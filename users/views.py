from django.shortcuts import render
from rest_framework.decorators import APIView, api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from .serializers import UserSerializer
from rest_framework.response import Response
from rest_framework_jwt.settings import api_settings, settings
from rest_framework import status
from .models import User
from django.contrib.auth.signals import user_logged_in
import jwt
from rest_framework.generics import RetrieveUpdateAPIView
from email_hunter import EmailHunterClient


jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

# Create your views here.


class CreateUserAPIView(APIView):
    permission_classes = (AllowAny, )

    def post(self, request):
        user = request.data
        serializer = UserSerializer(data=user)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['POST'])
@permission_classes([AllowAny, ])
def authenticate_user(request):
    try:
        email = request.data['email']
        password = request.data['password']

        user = User.objects.get(email=email, password=password)
        if user:
            try:
                playload = jwt_payload_handler(user)
                token = jwt.encode(playload, settings.SECRET_KEY)
                user_details = {}
                user_details['name'] = "%s %s" % (user.first_name, user.last_name)
                user_details['token'] = token
                user_logged_in.send(sender=user.__class__, request=request, user=user)
                return Response(user_details, status=status.HTTP_200_OK)
            except Exception as e:
                raise e
        else:
            result = {
                'error': 'can not authenticate with the given credentials or the account has been deactivated'
            }
            return Response(result, status=status.HTTP_403_FORBIDDEN)
    except KeyError:
        result = {
            'error': 'please provide a email and a password'
        }
        return Response(result)


class UserRetrieveUpdateAPIView(RetrieveUpdateAPIView):
    permission_classes = (IsAuthenticated, )
    serializer_class = UserSerializer

    def get(self, request, *args, **kwargs):
        serializer = self.serializer_class(request.user)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        serializer_data = request.data.get('user', {})
        serializer = UserSerializer(request.user, data=serializer_data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)