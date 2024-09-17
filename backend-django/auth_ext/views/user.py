from auth_ext.models.role import Role
from auth_ext.models.user import AuthExtUser
from auth_ext.serializers.user import (
    AuthExtTokenObtainPairSerializer,
    AuthRefreshTokenSerializer,
    AuthUserInfoSerializer,
    AuthUserPasswordSerializer,
    AuthUserSerializer,
)
from rest_framework import generics, status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView, TokenViewBase

from fast.settings import BASE_URL
from utils.storage import save_download_file, save_upload_file, save_upload_base64_file, file_system_storage


# 登录视图
class AuthExtUserView(TokenViewBase):
    serializer_class = AuthExtTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# 注册
class AuthUserViewSet(generics.GenericAPIView):
    serializer_class = AuthUserSerializer
    queryset = AuthExtUser.objects.all()
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 生成token
        token_serializer = AuthExtTokenObtainPairSerializer(data=request.data)
        token_serializer.is_valid(raise_exception=True)
        return Response(token_serializer.validated_data, status=status.HTTP_200_OK)


# 刷新token
class AuthRefreshToken(TokenRefreshView):
    serializer_class = AuthRefreshTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


# 用户信息
class AuthUserInfoViewSet(viewsets.ModelViewSet):
    queryset = AuthExtUser.objects.filter(is_deleted=False).all()
    serializer_class = AuthUserInfoSerializer
    permission_classes = []

    @action(detail=False, methods=['GET'])
    def mine(self, request):
        serializer = self.get_serializer(request.user)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @action(methods=["PUT"], detail=True)
    def change_password(self, request, pk=None):
        serializer = AuthUserPasswordSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.update(self.get_object(), serializer.validated_data)
        return Response(status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=True)
    def role_list(self, request, pk=None):
        obj = self.get_object()
        roles = obj.roles.all().values("id", "name")
        return Response(roles, status=status.HTTP_200_OK)

    @action(methods=["PUT"], detail=True)
    def add_roles(self, request, pk=None):
        obj = self.get_object()
        ids = request.data.get("ids")
        roles = Role.objects.filter(id__in=ids)
        obj.roles.set(roles)
        obj.save()
        return Response(status=status.HTTP_200_OK)

    @action(methods=["POST"], detail=True)
    def upload_avatar(self, request, pk=None):
        obj = self.get_object()
        avatar = request.data.get("base64")
        file_path = save_upload_base64_file(avatar,obj.username)
        obj.avatar = file_path
        obj.save()
        file_url = BASE_URL + file_system_storage.url(file_path)
        return Response({"avatar":file_url},status=status.HTTP_200_OK)

    @action(methods=["DELETE"], detail=False)
    def batch_delete(self, request):
        ids = request.data.get("ids")
        AuthExtUser.objects.filter(id__in=ids).update(is_deleted=True)
        return Response(status=status.HTTP_200_OK)
