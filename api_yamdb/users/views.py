from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import AccessToken, RefreshToken

from .constants import EMAIL_PROJECT
from .models import User
from .permissions import IsCustomAdmin
from .serializers import (TokenForUserSerializer, UserAdminSerializer,
                          UserCreateSerializer, UserUserSerializer)


class UsersViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserAdminSerializer
    permission_classes = [IsAuthenticated, IsCustomAdmin]
    lookup_field = 'username'
    filter_backends = [filters.SearchFilter]
    search_fields = ['username']

    @action(
        methods=['GET', 'PATCH'],
        detail=False,
        permission_classes=[IsAuthenticated],
        url_path='me'
    )
    def get_path_user(self, request):
        serializer = UserAdminSerializer(request.user)
        if request.method == 'PATCH':
            if request.user.is_admin:
                serializer = UserAdminSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            else:
                serializer = UserUserSerializer(
                    request.user,
                    data=request.data,
                    partial=True
                )
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(
                serializer.data, status=status.HTTP_200_OK
            )
        return Response(serializer.data)


class SignUpUser(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = UserCreateSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user_registrate = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        confirmation_code = default_token_generator.make_token(
            user_registrate
        )
        subject = 'Код подтверждения'
        message = (
            f'Ваш код подтверждения для регистрации: {confirmation_code}'
        )
        to = serializer.validated_data['email']
        from_email = EMAIL_PROJECT
        send_mail(subject, message, from_email, [str(to)])
        return Response(
            {'email': serializer.validated_data['email'],
             'username': serializer.validated_data['username']},
            status=status.HTTP_200_OK)


class TokenRegistrate(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = TokenForUserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user_registrate = get_object_or_404(
            User,
            username=serializer.validated_data['username']
        )
        if default_token_generator.check_token(
            user_registrate,
            serializer.validated_data['confirmation_code']
        ):
            token_acsess = AccessToken.for_user(user_registrate)
            token_refresh = RefreshToken.for_user(user_registrate)

            return Response(
                {
                    'Ваш персональный токен': str(token_acsess),
                    'Ваш refresh токен': str(token_refresh)
                },
                status=status.HTTP_200_OK
            )
        return Response(
            {'Неверный': 'confirmation_code'},
            status=status.HTTP_400_BAD_REQUEST
        )
