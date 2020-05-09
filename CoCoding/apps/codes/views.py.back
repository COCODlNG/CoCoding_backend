from rest_framework import mixins
from rest_framework.viewsets import GenericViewSet

from .serializers import CodeSerializer
from .models import Code


class CodeViewSet(mixins.CreateModelMixin,
                  mixins.RetrieveModelMixin,
                  GenericViewSet):

    serializer_class = CodeSerializer
    queryset = Code.objects.all()
