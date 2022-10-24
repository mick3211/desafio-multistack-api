from rest_framework import serializers
from ..models import Objeto


class ImagemObjetoSerializer(serializers.Serializer):
    imagem_objeto = serializers.ImageField(required=True)