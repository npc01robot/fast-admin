from rest_framework import serializers

from grid.models import Grid


class GridSerializer(serializers.ModelSerializer):
    class Meta:
        model = Grid
        fields = '__all__'