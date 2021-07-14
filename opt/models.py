from django.db import models
from custom_user.models import CustomUser

import datetime
class OTP(models):
    _type_otp = [
        ('verify_email','Verify Email Otp'),
        ('reset_password','Change Password Otp')
    ]
    otp = models.BigIntegerField(min_lenght = 5, max_length= 7, unique=True)
    user_id = models.ForeignKey(CustomUser,on_delete=models.CASCADE)
    expiring_time = models.DurationField(default=datetime.timedelta(minutes=5))
    created_time = models.DateTimeField(auto_now_add= True)
    type_otp = models.CharField(choices=_type_otp, null=False, blank=False)

    def is_expired(self):
        if (datetime.timezone.datetime)>(self.created_time + self.expiring_time):
            return True
        else:
            return False