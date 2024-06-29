import logging
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Task, Project
from ..serializers.serializers_v1 import TaskSerializer
from ..permissions.task_permission import IsTaskAssignee

logger = logging.getLogger(__name__)


class TaskViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsTaskAssignee]

    def get_queryset(self):
        if self.request.user.is_superuser:
            logger.info(f'Admin {self.request.user.username} is retrieving all tasks.')
            return Task.objects.all()
        logger.info(f'User {self.request.user.username} is retrieving their assigned tasks.')
        return Task.objects.filter(assigned_to=self.request.user)

    def get_serializer_class(self):
        return TaskSerializer

    def perform_create(self, serializer):
        project = get_object_or_404(Project, pk=self.request.data['project'])
        if self.request.user != project.created_by:
            logger.warning(
                f'User {self.request.user.username} tried to add a task to project {project.name} without permission.')
            raise PermissionDenied("You are not allowed to add tasks to this project.")
        serializer.save()
        logger.info(
            f'User {self.request.user.username} created task {serializer.instance.name} in project {project.name}.')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        logger.info(f'Task {serializer.instance.name} created by user {self.request.user.username}.')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f'User {self.request.user.username} listed tasks.')
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        logger.info(f'User {self.request.user.username} retrieved task {instance.name}.')
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info(f'User {self.request.user.username} updated task {instance.name}.')
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        logger.info(f'User {self.request.user.username} deleted task {instance.name}.')
        return Response(status=status.HTTP_204_NO_CONTENT)
