from rest_framework import viewsets, generics
from rest_framework.response import Response

from auth_ext.models.menu import Menu
from auth_ext.serializers.menu import MenuSerializer, MenuTreeSerializer


class MenuViewSet(viewsets.ModelViewSet):
    queryset = Menu.objects.filter(is_deleted=False).all()
    serializer_class = MenuSerializer
    permission_classes = []
    pagination_class = None

class MenuTreeViewSet(generics.ListAPIView):
    queryset = Menu.objects.filter(is_deleted=False).all()
    serializer_class = MenuTreeSerializer
    permission_classes = []

    def list(self, request, *args, **kwargs):
        serializer = self.get_serializer(self.get_queryset(), many=True)
        return Response(serializer.data)