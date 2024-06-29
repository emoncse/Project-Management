import logging
from rest_framework import viewsets, permissions, status
from rest_framework.exceptions import PermissionDenied
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from ..models import Project
from ..serializers.serializers_v1 import ProjectSerializer
from ..permissions.project_permission import IsProjectCreator

logger = logging.getLogger(__name__)


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, IsProjectCreator]

    def get_queryset(self):
        if self.request.user.is_superuser:
            logger.info(f'Admin {self.request.user.username} is retrieving all projects.')
            return Project.objects.all()
        logger.info(f'User {self.request.user.username} is retrieving their projects.')
        return Project.objects.filter(members=self.request.user)

    def get_serializer_class(self):
        return ProjectSerializer

    def perform_create(self, serializer):
        serializer.save(created_by=self.request.user)
        logger.info(f'User {self.request.user.username} created project {serializer.instance.name}.')

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        logger.info(f'Project {serializer.instance.name} created by user {self.request.user.username}.')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f'User {self.request.user.username} listed projects.')
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        logger.info(f'User {self.request.user.username} retrieved project {instance.name}.')
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info(f'User {self.request.user.username} updated project {instance.name}.')
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        logger.info(f'User {self.request.user.username} deleted project {instance.name}.')
        return Response(status=status.HTTP_204_NO_CONTENT)
