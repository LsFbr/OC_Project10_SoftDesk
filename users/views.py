from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from users.serializers import UserDetailSerializer, UserListSerializer, RegisterSerializer
from users.models import User

class AdminUserViewSet(ModelViewSet):
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    permission_classes = [IsAdminUser]

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class
        return self.detail_serializer_class 

class UserViewSet(ReadOnlyModelViewSet):
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    queryset = User.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class
        return self.detail_serializer_class
    

class RegisterView(CreateAPIView):

    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()

        refresh = RefreshToken.for_user(user)
        tokens = {
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }

        user_data = UserDetailSerializer(user).data
        return Response(
            {"user": user_data, "tokens": tokens},
            status=status.HTTP_201_CREATED
        )