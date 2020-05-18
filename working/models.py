from django.db import models
from django.contrib.auth.models import User


class Register(User):
    mobile = models.BigIntegerField(default=0, null=True, blank=True)

    def __str__(self):
        return self.first_name + self.last_name
