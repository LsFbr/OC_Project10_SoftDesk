from datetime import date
from rest_framework import serializers

from users.models import User


class UserListSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "username", "created_time"]
        read_only_fields = ["id", "created_time"]


class UserDetailSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["id", "username", "password", "birthday", "can_be_contacted", "can_data_be_shared", "created_time", "contributions", "authored_projects", "authored_issues", "assigned_issues", "authored_comments"]
        read_only_fields = ["id", "created_time", "contributions", "authored_projects", "authored_issues", "assigned_issues", "authored_comments"]

    def validate_birthday(self, value):
        if value is None:
            return
        today = date.today()
        years = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if years < 15:
            raise serializers.ValidationError("L'utilisateur doit avoir au moins 15 ans pour s'inscrire (RGPD).")
        
        return value

    def create(self, validated_data):
        pwd = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(pwd)
        user.save()
        return user

    def update(self, instance, validated_data):
        pwd = validated_data.pop("password", None)
        for attr, val in validated_data.items():
            setattr(instance, attr, val)
        if pwd:
            instance.set_password(pwd)
        instance.save()
        return instance

    def to_representation(self, instance):
        data = super().to_representation(instance)
        data["contributions"] = [{"id": contribution.id, "project": contribution.project.title} for contribution in instance.contributions.all()]
        data["authored_projects"] = [{"id": project.id, "title": project.title} for project in instance.authored_projects.all()]
        data["authored_issues"] = [{"id": issue.id, "title": issue.title} for issue in instance.authored_issues.all()]
        data["assigned_issues"] = [{"id": issue.id, "title": issue.title} for issue in instance.assigned_issues.all()]
        data["authored_comments"] = [{"id": comment.id, "description": comment.description} for comment in instance.authored_comments.all()]
        return data



class RegisterSerializer(serializers.ModelSerializer):
    # utilisé UNIQUEMENT pour la route d’inscription
    password = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = User
        fields = ["username", "password", "birthday", "can_be_contacted", "can_data_be_shared"]

    def validate_birthday(self, value):
        if value is None:
            raise serializers.ValidationError("La date de naissance est requise.")
        today = date.today()
        years = today.year - value.year - ((today.month, today.day) < (value.month, value.day))
        if years < 15:
            raise serializers.ValidationError("Vous devez avoir au moins 15 ans.")
        return value

    def create(self, validated_data):
        # hachage du mot de passe
        pwd = validated_data.pop("password")
        user = User(**validated_data)
        user.set_password(pwd)
        user.save()
        return user