from django.contrib.auth.tokens import default_token_generator
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import AccessToken

from .models import User
from .serializers import CodeConfSerializer, UserEmailSerializer
from .utils import sent_confirmation_code


@api_view(['POST'])
@permission_classes([AllowAny])
def create_user(request):
    serializer = UserEmailSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    email = serializer.validated_data['email']
    if User.objects.filter(username=username, email=email):
        sent_confirmation_code(username)
        return Response(
            {'email': email, 'username': username},
            status=status.HTTP_200_OK
        )
    serializer.save()
    sent_confirmation_code(username)
    return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([AllowAny])
def get_token(request):
    serializer = CodeConfSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    username = serializer.validated_data['username']
    confirmation_code = serializer.validated_data['confirmation_code']
    user = get_object_or_404(User, username=username)
    if default_token_generator.check_token(user, confirmation_code):
        token = AccessToken.for_user(user)
        return Response(
            {'token': str(token)},
            status=status.HTTP_200_OK
        )
    return Response(status=status.HTTP_400_BAD_REQUEST)
