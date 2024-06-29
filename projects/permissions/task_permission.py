from rest_framework import permissions


class IsTaskAssignee(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        return obj.assigned_to == request.user
