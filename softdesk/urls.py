from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from core.views import ContributorViewSet, ProjectViewSet, IssueViewSet, CommentViewSet
from users.views import UserViewSet, RegisterView, AdminUserViewSet

router = routers.SimpleRouter()

router.register('projects', ProjectViewSet, basename='project')
router.register('contributors', ContributorViewSet, basename='contributor')
router.register('issues', IssueViewSet, basename='issue')
router.register('comments', CommentViewSet, basename='comment')

router.register('users', UserViewSet, basename='user')
router.register('admin/users', AdminUserViewSet, basename='admin-user')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api-auth/', include('rest_framework.urls')),
    path('api/auth/register/', RegisterView.as_view(), name='auth-register'),
    path('api/auth/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/auth/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    path('api/', include(router.urls))
]

# Voir la librairie drf-nested-routers pour les urls imbriquées (https://github.com/alanjcastonguay/drf-nested-routers) 
# Par exemple : api/projects/1/contributors/
# api/projects/1/issues/
# api/projects/1/issues/1/comments/
# api/projects/1/issues/1/comments/1/