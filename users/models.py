from django.contrib.auth.models import AbstractUser
from django.core.exceptions import ValidationError
from django.db import models
from datetime import date


def validate_age(birthday: date):
    if birthday is None:
        return
    today = date.today()
    years = today.year - birthday.year - ((today.month, today.day) < (birthday.month, birthday.day))
    if years < 15:
        raise ValidationError("L'utilisateur doit avoir au moins 15 ans pour s'inscrire (RGPD).")


class User(AbstractUser):
    email = None
    first_name = None
    last_name = None
    birthday = models.DateField(validators=[validate_age])
    can_be_contacted = models.BooleanField(default=False)
    can_data_be_shared = models.BooleanField(default=False)
    created_time = models.DateTimeField(auto_now_add=True)

    EMAIL_FIELD = None
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.username
