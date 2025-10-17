from rest_framework.viewsets import ModelViewSet
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.generics import CreateAPIView
from rest_framework_simplejwt.tokens import RefreshToken

from users.serializers import UserSerializer, RegisterSerializer
from users.models import User

class UserViewSet(ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects.all()

    permission_classes = [IsAuthenticated]
    

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

        user_data = UserSerializer(user).data
        return Response(
            {"user": user_data, "tokens": tokens},
            status=status.HTTP_201_CREATED
        )