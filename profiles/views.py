from rest_framework import viewsets
from django.contrib.auth import get_user_model
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.generics import GenericAPIView, CreateAPIView, RetrieveAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.authtoken.models import Token

from base.emails import EmailService
from base.roles_permissions import IsSuperUser
from base.utils import random_password
from profiles.serializers import UserSerializer, LoginSerializer, VerifyUserSerializer, VerificationSerializer

User = get_user_model()


class UserViewSet(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsSuperUser,)


class VerificationView(GenericAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = VerificationSerializer

    def post(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        EmailService.send_verification_email(
            serializer.data.get("email"),
            "first_name",
            Token.objects.get_or_create(user=serializer.user_)[0]
        )
        serializer.user_.is_active = True
        serializer.user_.save()
        return Response({"detail": "Verification Email was sent"})


class LoginView(ObtainAuthToken):
    serializer_class = LoginSerializer
    permission_classes = (AllowAny,)

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user': {
                # 'user_id': user.pk,
                'email': user.email,
                'first_name': user.first_name,
                'last_name': user.last_name
            }
        })


class VerifyUserView(GenericAPIView):
    permission_classes = (IsSuperUser,)
    serializer_class = VerifyUserSerializer

    def post(self, request, *args, **kwargs):
        return Response({})
        # random_password


class ProfileDetailsView(RetrieveAPIView):
    serializer_class = UserSerializer
    permission_classes = (IsAuthenticated,)

    def get_object(self):
        return self.request.user
