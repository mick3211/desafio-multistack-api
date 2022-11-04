from rest_framework import serializers
from ..models import Local
from ..hateoas import Hateoas
from django.urls import reverse


class LocaisBuscaSerializer(serializers.ModelSerializer):

    links = serializers.SerializerMethodField(read_only=True)
    imagem = serializers.ImageField(source="imagem_local", read_only=True)


    class Meta:
        model = Local
        fields = ('id', 'nome', 'endereco', 'contato', 'descricao', 'imagem', 'links')

    
    def get_links(self, obj):
        links = Hateoas()
        links.add_get('objetos_local', reverse('objetos-local-list', kwargs={'local_id': obj.id}))
        return links.to_array()