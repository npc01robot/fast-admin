from auth_ext.models.menu import Menu
from rest_framework import serializers


class MenuSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Menu
        fields = "__all__"


class MenuTreeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Menu
        fields = ("id", "parent", "menu_type", "title")
