from auth_ext.models.role import Role
from auth_ext.serializers.role import (
    RoleListSerializer,
    RoleMenuSerializer,
    RoleSerializer,
)
from rest_framework import generics, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response


class RoleViewSet(viewsets.ModelViewSet):
    queryset = Role.objects.filter(is_deleted=False).all()
    serializer_class = RoleSerializer
    permission_classes = []

    @action(detail=True, methods=["GET"])
    def menu_list(self, request, pk=None):
        role = self.get_object()
        serializer = RoleMenuSerializer(role, many=False)
        return Response(serializer.data)

    @action(detail=True, methods=["PUT"])
    def menu_update(self, request, pk=None):
        role = self.get_object()
        serializer = RoleMenuSerializer(data=request.data, instance=role)
        serializer.is_valid(raise_exception=True)
        serializer.update(role, serializer.validated_data)
        return Response(serializer.data)

    @action(detail=False, methods=["GET"])
    def role_list(self, request):
        roles = self.get_queryset()
        serializer = RoleListSerializer(roles, many=True)
        return Response(serializer.data)
