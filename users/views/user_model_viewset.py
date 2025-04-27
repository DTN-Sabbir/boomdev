from rest_framework import viewsets

from rest_framework.permissions import IsAuthenticated, AllowAny

from users.serializers.user_model_serializer import (
    UserModelCreateSerializer,
    UserUpdateSerializer,
    UserRetrieveSerializer,
    UserListSerializer,
    UserModelDeleteSerializer,
)
from users.models import CustomUser


class UserModelViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """

    def get_permissions(self):
        """
        Instantiates and returns the list of permissions that this view requires.
        """
        if self.action in ["create", "update", "partial_update", "destroy"]:
            self.permission_classes = [IsAuthenticated]
        else:
            self.permission_classes = [AllowAny]
        return super().get_permissions()

    def get_serializer_class(self):
        """
        Returns the serializer class to be used for the request.
        """
        if self.action == "create":
            return UserModelCreateSerializer
        elif self.action in ["update", "partial_update"]:
            return UserUpdateSerializer
        elif self.action == "retrieve":
            return UserRetrieveSerializer
        elif self.action == "list":
            return UserListSerializer
        elif self.action == "destroy":
            return UserModelDeleteSerializer
        return super().get_serializer_class()

    def get_queryset(self):
        queryset = CustomUser.objects.all()
        if self.action == "list":
            queryset = queryset.filter(is_active=True)
        elif self.action == "retrieve":
            queryset = queryset.filter(is_active=True)
        elif self.action == "destroy":
            queryset = queryset.filter(is_active=True)
        elif self.action == "update":
            queryset = queryset.filter(is_active=True)
        elif self.action == "create":
            queryset = queryset.filter(is_active=True)
        return queryset
