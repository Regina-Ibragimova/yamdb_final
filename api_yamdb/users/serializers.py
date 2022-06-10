from rest_framework import serializers

from .models import User


class UserEmailSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email', 'username')

    def validate_username(self, value):
        if value == 'me':
            raise serializers.ValidationError(
                'this field should not be called <me>'
            )
        return value


class CodeConfSerializer(serializers.Serializer):
    username = serializers.CharField()
    confirmation_code = serializers.CharField()
