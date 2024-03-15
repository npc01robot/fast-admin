from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework_simplejwt.views import TokenViewBase, TokenRefreshView

from auth_ext.models import AuthExtUser
from auth_ext.serializers import AuthExtTokenObtainPairSerializer, AuthUserSerializer, AuthRefreshTokenSerializer


# Create your views here.

class AuthExtUserView(TokenViewBase):
    serializer_class = AuthExtTokenObtainPairSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class AuthUserViewSet(generics.GenericAPIView):
    serializer_class = AuthUserSerializer
    queryset = AuthExtUser.objects.all()
    permission_classes = []

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()

        # 生成token
        token_serializer = AuthExtTokenObtainPairSerializer(
            data=request.data
        )
        token_serializer.is_valid(raise_exception=True)
        return Response(token_serializer.validated_data, status=status.HTTP_200_OK)


class AuthRefreshToken(TokenRefreshView):
    serializer_class = AuthRefreshTokenSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        return Response(serializer.validated_data, status=status.HTTP_200_OK)


class AsyncRoute(generics.GenericAPIView):
    """
    动态生成路由,大型项目使用
    """

    def get(self, request, *args, **kwargs):
        user = AuthExtUser.objects.filter(pk=request.auth.payload['user_code']).first()
        data = [
            {
                "path": "/drawing",
                "redirect": "/drawing/index",
                "rank": 9,
                "meta": {
                    "icon": "informationLine",
                    "title": "实际贷款情况",
                    "showLink": False
                },
                "children": [
                    {
                        "path": "/drawing/index",
                        "name": "drawing",
                        "meta": {
                            "title": "实际贷款情况",
                            "roles": user.roles,
                            "auths": user.auths
                        }
                    }
                ]
            },
            {
                "path": "/assure",
                "redirect": "/assure/index",
                "rank": 9,
                "meta": {
                    "icon": "informationLine",
                    "title": "对外担保"
                },
                "children": [
                    {
                        "path": "/assure/index",
                        "name": "assure",
                        "meta": {
                            "title": "对外担保",
                            "roles": user.roles,
                            "auths": user.auths
                        }
                    }
                ]
            },
            {
                "path": "/funds",
                "redirect": "/funds/index",
                "rank": 99,
                "meta": {
                    "icon": "informationLine",
                    "title": "融资情况"
                },
                "children": [
                    {
                        "path": "/funds/index",
                        "name": "funds",
                        "meta": {
                            "title": "融资情况",
                            "roles": user.roles,
                            "auths": user.auths
                        }
                    }
                ]
            }
        ]
        return Response(data=data)
