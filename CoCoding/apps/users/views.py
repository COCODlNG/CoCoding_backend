from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.response import Response


class LoginView(ObtainAuthToken):
    def post(self, request, *args, **kwargs):
        # todo: 로그인시에 띄워줄 기본정보 필요시에 이 부분 오버라이딩
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({'token': token.key})

