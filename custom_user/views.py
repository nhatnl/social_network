

from allauth.account.adapter import get_adapter
from allauth.utils import email_address_exists

from django.utils.translation import ugettext_lazy as _
from django.views.generic import DetailView
from django.shortcuts import get_object_or_404

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status


from .serializers import UserSerializer
from .models import CustomUser
from .serializers import EmailSerializer, VerifyEmailSerializer

from rest_auth.registration.views import RegisterView
from allauth.account.views import ConfirmEmailView
from allauth.account.models import EmailConfirmationHMAC, EmailAddress

class CustomRegisterView(RegisterView):
    pass

class CustomVerifyView(APIView, ConfirmEmailView):
    def get_serializer(self, *args, **kwargs):
        return VerifyEmailSerializer(*args, **kwargs)
    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.kwargs['key'] = serializer.validated_data['key']
        confirmation = self.get_object()
        confirmation.confirm(self.request)
        return Response({'detail': _('ok')}, status=status.HTTP_200_OK)

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

class DetailUserView(APIView):
    model = CustomUser

    def get(self, request, *args, **kwargs):
        obj = get_object_or_404(self.model, pk = request.user.id)
        data = {
            "email": obj.email,
            "first_name": obj.first_name,
            "last_name": obj.last_name,
            "age": obj.age
        }
        return Response(data=data)

class DetailUserAdminView(APIView):
    model =CustomUser

    def get(self, request, *args, **kwargs):
        if request.user.is_superuser:
            obj = get_object_or_404(self.model, pk = kwargs['pk'])
            data = {
            "email": obj.email,
            "first_name": obj.first_name,
            "last_name": obj.last_name,
            "age": obj.age
            }
            return Response(data=data, status=status.HTTP_200_OK)
        else:
            adp = get_adapter(request)
            return Response(data={'message':'Permission Denied'}, status=status.HTTP_400_BAD_REQUEST)