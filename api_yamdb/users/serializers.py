from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from users.models import User
from users.validations import validate_username


class UserAdminSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('username', 'email', 'first_name',
                  'last_name', 'bio', 'role')

        def validate_username(self, value):
            return validate_username(self, value)


class UserUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'username',
            'email',
            'first_name',
            'last_name',
            'bio',
            'role'
        )
        read_only_fields = ['role']

    def validate_username(self, value):
        return validate_username(self, value)


class UserCreateSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(
        validators=[UniqueValidator(queryset=User.objects.all())]
    )

    class Meta:
        model = User
        fields = (
            'username', 'email', 'role'
        )
        read_only_fields = ['role']

    def validate_username(self, value):
        return validate_username(self, value)


class TokenForUserSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=150, required=True)
    confirmation_code = serializers.CharField(max_length=1000, required=True)

    def validate_username(self, value):
        return validate_username(self, value)
