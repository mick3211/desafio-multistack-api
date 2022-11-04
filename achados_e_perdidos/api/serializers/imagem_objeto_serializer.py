from rest_framework import serializers


class ImagemObjetoSerializer(serializers.Serializer):
    imagem_objeto = serializers.ImageField(required=True)