from rest_framework import serializers
from rest_framework.utils.representation import smart_repr
from django.utils.translation import gettext as _

class AgeAtLeast18:
    """
        Validation For Checking If User Age as least 18
    """
    message =_('User under 18 years old, current ages: {age}')
    def __init__(self, age_field='age', message=None) -> None:
        self.age_field = age_field
        self.message = message or self.message

    def __call__(self, attrs):
        if attrs[self.age_field]<18:
            message = self.message.format(age=self.age_field)
            raise serializers.ValidationError(message, code='age_under_18')

# class PasswordValidation:
#     """
#         Validation For password has as least 8 char mus has number and character
#     """
#     message = _('password must has 8 char length and has number and alphabe char')

#     def __init__(self, password_field = ) -> None:
        