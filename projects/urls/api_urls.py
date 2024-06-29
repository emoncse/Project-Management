from rest_framework.routers import DefaultRouter
from ..views.api_user_views import UserViewSet
from ..views.api_project_views import ProjectViewSet
from ..views.api_task_views import TaskViewSet

router = DefaultRouter()
router.register(r'users', UserViewSet, basename='user')
router.register(r'projects', ProjectViewSet, basename='project')
router.register(r'tasks', TaskViewSet, basename='task')

urlpatterns = router.urls
