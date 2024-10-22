from auth_ext.models.role import Role
from rest_framework import serializers


class RoleSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)

    class Meta:
        model = Role
        fields = "__all__"


class RoleMenuSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    menu_list = serializers.SerializerMethodField()

    def get_menu_list(self, obj):
        return obj.menu.all().values_list("id", flat=True)

    class Meta:
        model = Role
        fields = ["id", "menu_list"]

    def update(self, instance, validated_data):
        menu_list = self.initial_data.get("menu_list")
        if menu_list is not None:
            instance.menu.set(menu_list)
        return super().update(instance, validated_data)


class RoleListSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(read_only=True)
    name = serializers.CharField(read_only=True)

    class Meta:
        model = Role
        fields = ["id", "name"]
