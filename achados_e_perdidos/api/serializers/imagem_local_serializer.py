from rest_framework import serializers
from ..services.local_service import get_local_by_user_id


class ImagemLocalSerializer(serializers.Serializer):
    imagem_local = serializers.ImageField()

    def create(self, validated_data):
        local = get_local_by_user_id(self.context['user'].id)
        local.imagem_local = validated_data['imagem_local']
        local.save()
        return validated_data