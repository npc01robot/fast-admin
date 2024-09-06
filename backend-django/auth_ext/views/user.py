from auth_ext.models.user import AuthExtUser
from auth_ext.serializers.user import (
    AuthExtTokenObtainPairSerializer,
    AuthRefreshTokenSerializer,
    AuthUserSerializer,
)
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenRefreshView, TokenViewBase


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
class AuthUserInfoView(generics.RetrieveAPIView):
    serializer_class = AuthUserSerializer
    queryset = AuthExtUser.objects.all()
    permission_classes = []

    def get_object(self):
        return self.request.user
