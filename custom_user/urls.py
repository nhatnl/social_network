from django.views.generic import TemplateView
from django.conf.urls import url

from .views import RegisterView, CustomVerifyView, ReCreateKeyVerifyEmail

urlpatterns = [
    url(r'^register/$', RegisterView.as_view(), name='custom_rest_register'),
    url(r'^verify/$', CustomVerifyView.as_view(), name='custom_rest_verify_email'),
    url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
        name='account_confirm_email'),
    url(r'^resent-confirm-email/$', ReCreateKeyVerifyEmail.as_view(), name='recreate_key_email')
]