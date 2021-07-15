from custom_user.models import CustomUser

from allauth.account.adapter import DefaultAccountAdapter, get_adapter

class CustomAdapter(DefaultAccountAdapter):
    pass