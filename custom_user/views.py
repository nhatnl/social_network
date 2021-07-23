

from allauth.account.adapter import get_adapter
from allauth.utils import email_address_exists

from django.utils.translation import ugettext_lazy as _
from django.shortcuts import get_object_or_404


from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.generics import RetrieveUpdateDestroyAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated, IsAdminUser


from .serializers import UserSerializer
from .models import CustomUser
from .serializers import EmailSerializer, VerifyEmailSerializer

from rest_auth.registration.views import RegisterView, LoginView
from rest_auth.views import LogoutView, PasswordChangeView, PasswordResetView, PasswordResetConfirmView

from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailConfirmationHMAC, EmailAddress

class CustomRegisterView(RegisterView):
    pass

class CustomVerifyView(APIView, ConfirmEmailView):

    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)


class ReCreateKeyVerifyEmail(APIView):

    def get_serializer(self, *args, **kwargs):
        return EmailSerializer(*args, **kwargs)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['email'] = serializer.validated_data['email']
        if email_address_exists(self.kwargs['email']):
            email_obj = EmailConfirmationHMAC(EmailAddress.objects.get(email=self.kwargs['email']))
            email_obj.send()
            return Response({'detail': _('ok')}, status=status.HTTP_200_OK)
        else:
            return Response({'detail': _('Nope')}, status=status.HTTP_400_BAD_REQUEST)

class CustomLogin(LoginView):
    pass

class CustomLogout(LogoutView):
    pass

class CustomChangePassword(PasswordChangeView):
    pass

class CustomResetPassword(PasswordResetView):
    pass

class CustomResetPasswordConfirm(PasswordResetConfirmView):
    pass

class CustomDetailUser(RetrieveUpdateAPIView):
    model = CustomUser
    permission_classes = [IsAuthenticated]
    queryset = model.objects
    def get_serializer(self, *args, **kwargs):
        return UserSerializer(*args,**kwargs)
    
    def get_object(self):
        return self.request.user

class CustomDetailUserAdmin(RetrieveUpdateDestroyAPIView):
    model = CustomUser
    permission_classes = [IsAuthenticated]
    queryset = model.objects
    def get_serializer(self, *args, **kwargs):
        return UserSerializer(*args,**kwargs)

class ListUser(ListAPIView):
    model = CustomUser
    permission_classes = [IsAuthenticated]
    
    def get_queryset(self):
        return self.model.objects.all().exclude(id = self.request.user.id)
    
    def get_serializer_class(self):
        return UserSerializer