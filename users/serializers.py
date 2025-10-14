from datetime import date
from rest_framework import serializers

from users.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "password", "birthday", "can_be_contacted", "can_data_be_shared", "created_time", "contributions", "authored_projects", "authored_issues", "authored_comments", "assigned_issues"]

        read_only_fields = ["password", "created_time"]

        def validate_birthday(self, value):
            if value is None:
                return
            today = date.today()
            years = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
            if years < 15:
                raise serializers.ValidationError("L'utilisateur doit avoir au moins 15 ans pour s'inscrire (RGPD).")
