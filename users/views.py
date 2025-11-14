from rest_framework.viewsets import ModelViewSet, ReadOnlyModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny, IsAdminUser
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework import status

from users.serializers import UserDetailSerializer, UserListSerializer, RegisterSerializer
from users.models import User
from users.permissions import IsSelfOrSuperuserOrReadOnly

class UserViewSet(ModelViewSet):
    serializer_class = UserListSerializer
    detail_serializer_class = UserDetailSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated, IsSelfOrSuperuserOrReadOnly]

    def get_serializer_class(self):
        if self.action == "list":
            return self.serializer_class
        return self.detail_serializer_class

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        user_id = instance.id
        username = instance.username

        self.perform_destroy(instance)

        return Response(
            {"detail": f"User '{username}'(id={user_id}) deleted."},
            status=status.HTTP_200_OK
        )
    

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