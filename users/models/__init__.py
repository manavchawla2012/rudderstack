from typing import Union

from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import UserManager
from django.db import models

from rudderstack.fields.base_model_fields import BaseModelFields
from rudderstack.validators import Validators
from users.apps import UsersConfig as AppConfig
from business.models import BusinessModel


class UserModel(BaseModelFields, AbstractBaseUser):
    USERNAME_FIELD = 'email_id'

    first_name = models.CharField(max_length=100, null=False, blank=False)
    last_name = models.CharField(max_length=100, null=False, blank=False)
    middle_name = models.CharField(max_length=100, null=True, blank=False)
    email_id = models.EmailField(max_length=100, null=False, blank=False, unique=True,
                                 validators=[Validators.email_validator])
    mobile = models.CharField(max_length=10, null=False, blank=False, unique=True,
                              validators=[Validators.mobile_validator])
    image_url = models.CharField(max_length=1000, null=True, blank=True)
    password = models.CharField(max_length=128, null=True, blank=False)
    created_by = models.ForeignKey("self", null=True, blank=True, on_delete=models.DO_NOTHING)
    is_admin = models.BooleanField(null=False, blank=False, default=False)
    is_staff = models.BooleanField(null=False, blank=False, default=False)

    objects = UserManager()

    class Meta:
        managed = True
        db_table = str(AppConfig.name)

    def business(self) -> Union[BusinessModel, None]:
        return BusinessModel.objects.filter(business_owner=self.id).first()
