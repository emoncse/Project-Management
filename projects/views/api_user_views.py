import logging
from rest_framework import viewsets, permissions, status
from rest_framework.response import Response
from django.contrib.auth.models import User
from ..serializers.serializers_v1 import UserSerializer

logger = logging.getLogger(__name__)


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        logger.info(f'User {self.request.user.username} is retrieving the user list.')
        return User.objects.all()

    def get_serializer_class(self):
        return UserSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        logger.info(f'User {request.user.username} created new user {serializer.instance.username}.')
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = self.get_serializer(queryset, many=True)
        logger.info(f'User {request.user.username} listed users.')
        return Response(serializer.data)

    def retrieve(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        serializer = self.get_serializer(instance)
        logger.info(f'User {request.user.username} retrieved details for user {instance.username}.')
        return Response(serializer.data)

    def update(self, request, pk=None, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = self.get_serializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        logger.info(f'User {request.user.username} updated user {instance.username}.')
        return Response(serializer.data)

    def destroy(self, request, pk=None, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        logger.info(f'User {request.user.username} deleted user {instance.username}.')
        return Response(status=status.HTTP_204_NO_CONTENT)
