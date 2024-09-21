from rest_framework import viewsets

from grid.models import Grid
from grid.serializers import GridSerializer


class GridViewSet(viewsets.ModelViewSet):
    queryset = Grid.objects.all()
    serializer_class = GridSerializer
