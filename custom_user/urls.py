
from django.urls.conf import path
from django.views.generic import TemplateView
from django.conf.urls import url

from .views import (
    CustomLogout,
    CustomRegisterView,
    CustomResetPasswordConfirm, 
    CustomVerifyView, 
    ReCreateKeyVerifyEmail, 
    CustomLogin, 
    CustomDetailUser, 
    CustomDetailUserAdmin,
    CustomChangePassword,
    CustomResetPassword,
    ListUser

)

urlpatterns = [
    path('', ListUser.as_view(), name= 'list_user'),
    url(r'^register/$', CustomRegisterView.as_view(), name='custom_rest_register'),
    url(r'^verify/$', CustomVerifyView.as_view(), name='custom_rest_verify_email'),
    # url(r'^account-confirm-email/(?P<key>[-:\w]+)/$', TemplateView.as_view(),
    #     name='account_confirm_email'),
    # url(r'^resent-confirm-email/$', ReCreateKeyVerifyEmail.as_view(), name='recreate_key_email'),
    url(r'^login/$', CustomLogin.as_view(), name='custom_login'),
    url(r'^logout/$', CustomLogout.as_view(), name='custom_logout'),
    url(r'^me/$', CustomDetailUser.as_view(), name='custom_detail_user'),
    path('<int:pk>/', CustomDetailUserAdmin.as_view(), name='custom_detail_user_admin'),
    path('me/change-password/',CustomChangePassword.as_view(), name='custom_change_password'),
    path('reset-password/',CustomResetPassword.as_view(), name='custom_reset_password'),
    path('reset-password/confirm/<uidb64>/<token>', CustomResetPasswordConfirm.as_view(), name='password_reset_confirm'),
    
    

]