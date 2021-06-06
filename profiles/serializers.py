from django.contrib.auth import get_user_model
from rest_framework import serializers
from django.utils.translation import gettext_lazy as _
from django.contrib.auth import authenticate
from rest_framework.exceptions import ValidationError

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'is_staff', "al_id", "is_active"]
        read_only_fields = ['id', "is_active"]


class VerificationSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(required=True)
    def validate_email(self, value):
        self.user_ = User.objects.filter(email=value).first()
        if not self.user_:
            raise ValidationError("User doesn't exist")
        return value

    class Meta:
        model = User
        fields = ['email']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(write_only=True)
    password = serializers.CharField(trim_whitespace=False, write_only=True)
    token = serializers.CharField(read_only=True)

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')

        if email and password:
            user = authenticate(request=self.context.get('request'),
                                email=email, password=password)

            # The authenticate call simply returns None for is_active=False
            # users. (Assuming the default ModelBackend authentication
            # backend.)
            if not user:
                msg = _('Unable to log in with provided credentials.')
                raise serializers.ValidationError(msg, code='authorization')
        else:
            msg = _('Must include "email" and "password".')
            raise serializers.ValidationError(msg, code='authorization')

        attrs['user'] = user
        return attrs


class VerifyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['email']
